# file: backend/bot_embedding.py
from search import search_by_keyphrase, get_related_questions
from database import save_feedback
from sentence_transformers import SentenceTransformer
from transformers import AutoTokenizer, AutoModelForSeq2SeqLM
import torch
import torch.nn.functional as F
import html
import re

# ===== CPU/GPU setup =====
DEVICE = "cuda" if torch.cuda.is_available() else "cpu"

# Embedding model (VN-Law)
EMBED_MODEL_NAME = "truro7/vn-law-embedding"
embed_model = SentenceTransformer(EMBED_MODEL_NAME)
embed_model.to(DEVICE)

# LLM for answer generation (lightweight)
LLM_NAME = "VietAI/vit5-base"
llm_tokenizer = AutoTokenizer.from_pretrained(LLM_NAME)
llm_model = AutoModelForSeq2SeqLM.from_pretrained(
    LLM_NAME, device_map="auto", torch_dtype=torch.float16
).to(DEVICE)

conversation_history = {}

# ===== Utils =====
def sanitize(text):
    return html.escape(text)

def highlight_keyphrases(text, keyphrases):
    for i, kp in enumerate(keyphrases):
        if not kp:
            continue
        safe_kp = re.escape(kp)
        pattern = re.compile(r'(' + safe_kp + r')', flags=re.IGNORECASE)
        color = ["#f44336", "#2196F3", "#4CAF50", "#FF9800"][i % 4]
        text = pattern.sub(f"<span style='color:{color};font-weight:bold'>\\1</span>", text)
    return text

def clean_text(text):
    text = re.sub(r'[^\w\s.,;:?!\u00C0-\u1EF9]', '', text)
    return re.sub(r'\s+', ' ', text).strip()

def is_meaningful_text(text):
    return bool(re.search(r'[\w\u00C0-\u1EF9]', text))

# ===== Embedding-based semantic search =====
def semantic_search(query, corpus_texts, top_k=2):
    """
    query: str
    corpus_texts: list of str
    return: list of top_k texts
    """
    query_emb = embed_model.encode([query], convert_to_tensor=True)
    corpus_emb = embed_model.encode(corpus_texts, convert_to_tensor=True)
    cosine_scores = F.cosine_similarity(query_emb, corpus_emb)
    topk = torch.topk(cosine_scores, k=min(top_k, len(corpus_texts)))
    return [corpus_texts[i] for i in topk.indices]

# ===== LLM Generation =====
def llm_generate(context, query, max_new_tokens=256):
    context = clean_text(context.replace("\n", " "))
    if not is_meaningful_text(context):
        return "[CHÚ Ý] Không có thông tin hợp lệ trong context để trả lời chính xác."
    
    prompt = (
        f"Bạn là trợ lý pháp luật Việt Nam. Trả lời ngắn gọn, chính xác, tiếng Việt có dấu.\n\n"
        f"Văn bản tham khảo:\n{context}\n\nCâu hỏi: {query}\nTrả lời:"
    )
    
    inputs = llm_tokenizer(prompt, return_tensors="pt").to(DEVICE)
    outputs = llm_model.generate(
        **inputs,
        max_new_tokens=max_new_tokens,
        do_sample=False,
        num_beams=3,
        no_repeat_ngram_size=3,
        early_stopping=True,
        length_penalty=1.0
    )
    ans = llm_tokenizer.decode(outputs[0], skip_special_tokens=True)
    return clean_text(ans.replace(prompt, "").strip())

def guardrail_check(answer_text, source_texts):
    lowered = answer_text.lower()
    for s in source_texts:
        for token in s.split()[:6]:
            if token.lower() in lowered:
                return answer_text
    return "[CHÚ Ý] Câu trả lời suy luận; vui lòng kiểm tra văn bản gốc:\n\n" + answer_text

# ===== Main QA function =====
def answer_question(user_id, question, law_corpus=[]):
    """
    law_corpus: list of dicts {'noi_dung': ..., 'chuong': ..., 'dieu': ...}
    """
    history = conversation_history.get(user_id, [])
    context_history = " ".join(history[-2:])
    
    # 1. Keyphrase search
    kp_results = search_by_keyphrase(question)
    if kp_results:
        item = kp_results[0]
        highlighted = highlight_keyphrases(item.get("noi_dung",""), item.get("keyphrase", []))
        answer = f"{item.get('chuong','')}, Điều {item.get('dieu','')}: {highlighted}"
        related = get_related_questions(question)
        history.append(question)
        conversation_history[user_id] = history
        return sanitize(answer), related
    
    # 2. Embedding semantic search
    if law_corpus:
        corpus_texts = [doc["noi_dung"] for doc in law_corpus]
        top_docs = semantic_search(question, corpus_texts, top_k=2)
        if top_docs:
            llm_ans = llm_generate("\n".join(top_docs), question)
            checked = guardrail_check(llm_ans, top_docs)
            related = get_related_questions(question)
            history.append(question)
            conversation_history[user_id] = history
            return sanitize(checked), related
    
    # 3. fallback
    history.append(question)
    conversation_history[user_id] = history
    return "Xin lỗi, chưa tìm thấy thông tin phù hợp.", []

# ===== Feedback learning =====
def learn_from_feedback(question, answer_text, user_id="anonymous"):
    save_feedback(question, answer_text, user=user_id)
