# backend/bot.py
from search import search_by_keyphrase, search_semantic, get_related_questions, fuzzy_search, load_docs
from database import save_feedback
import html
import re
from transformers import AutoTokenizer, AutoModelForCausalLM
import torch

conversation_history = {}

# ===== Device setup =====
device = "cuda" if torch.cuda.is_available() else "cpu"
print(f"[INFO] Using device: {device}")

llm_tokenizer = AutoTokenizer.from_pretrained("Qwen/Qwen1.5-1.8B-Chat")
llm_model = AutoModelForCausalLM.from_pretrained("Qwen/Qwen1.5-1.8B-Chat").to(device)

# ===== Utils =====
def sanitize(text):
    return html.escape(text)

def highlight_keyphrases(text, keyphrases):
    """Highlight các keyphrase bằng màu đẹp"""
    for i, kp in enumerate(keyphrases):
        if not kp:
            continue
        safe = re.escape(kp)
        color = ["#f44336", "#2196F3", "#4CAF50", "#FF9800"][i % 4]
        text = re.sub(
            r"(" + safe + r")",
            rf"<span style='color:{color};font-weight:bold'>\1</span>",
            text,
            flags=re.IGNORECASE
        )
    return text

# ===== Main QA =====
def answer_question(user_id, question, law_corpus=None):
    history = conversation_history.get(user_id, [])

    # ===== 1. Keyphrase search =====
    kp = search_by_keyphrase(question)
    if kp:
        item = kp[0]
        content = highlight_keyphrases(item["noi_dung"], item.get("keyphrase", []))
        answer = f"{item['chuong']}, Điều {item['dieu']}: {content}"
        related = get_related_questions(question)
        if question not in history:
            history.append(question)
        conversation_history[user_id] = history
        return answer, related

    # ===== 2. Fuzzy search =====
    if law_corpus:
        fuzzy = fuzzy_search(question, law_corpus)
        if fuzzy:
            d = fuzzy[0]
            if question not in history:
                history.append(question)
            conversation_history[user_id] = history
            return f"{d['chuong']}, Điều {d['dieu']}: {d['noi_dung']}", []

    # ===== 3. Semantic search (top-3, filter low score) =====
    sem = search_semantic(question, top_k=3)
    sem = [d for d in sem if d.get("score", 0) >= 0.3]

    if sem:
        # Lọc trùng nội dung
        seen = set()
        unique_docs = []
        for d in sem:
            key = d["noi_dung"]
            if key not in seen:
                seen.add(key)
                unique_docs.append(d)

        enhanced = llm_enhance_answer(question, unique_docs, history)
        related = [d["noi_dung"] for d in unique_docs[1:]]
        if question not in history:
            history.append(question)
        conversation_history[user_id] = history
        return enhanced, related

    # ===== 4. Fallback =====
    if question not in history:
        history.append(question)
    conversation_history[user_id] = history
    return "Không tìm thấy nội dung phù hợp trong luật.", []

# ===== Feedback =====
def learn_from_feedback(question, answer_text, user_id="anonymous"):
    save_feedback(question, answer_text, user=user_id)

# ===== LLM answer enhancement =====
def llm_enhance_answer(question, law_items, history=[]):
    """
    law_items: list of dict {chuong, dieu, noi_dung}
    history: list of previous questions, để LLM tránh lặp
    """
    context = "\n".join([f"- {d['chuong']} Điều {d['dieu']}: {d['noi_dung']}" 
                         for d in law_items])

    # History giới hạn 5 câu gần nhất
    recent_qs = "\n".join(history[-5:]) if history else "Không có câu hỏi trước"

    prompt = (
        "Bạn là trợ lý luật đất đai.\n"
        f"Câu hỏi hiện tại: {question}\n"
        f"Các đoạn luật liên quan:\n{context}\n"
        f"Các câu hỏi gần đây của người dùng:\n{recent_qs}\n"
        "Hãy giải thích rõ ràng, dễ hiểu, súc tích dựa trên luật ở trên (không bịa).\n"
    )

    inputs = llm_tokenizer(prompt, return_tensors="pt").to(device)
    out = llm_model.generate(**inputs, max_new_tokens=150, do_sample=True, temperature=0.7)
    return llm_tokenizer.decode(out[0], skip_special_tokens=True)
