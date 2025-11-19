import html, re
from search import search_by_keyphrase, search_semantic, get_related_questions, fuzzy_search
from database import save_feedback

conversation_history = {}

def sanitize(text):
    return html.escape(text)

def highlight_keyphrases(text, keyphrases):
    for kp in keyphrases:
        if not kp: continue
        safe = re.escape(kp)
        text = re.sub(r"("+safe+r")", r"<span class='law-highlight'>\1</span>", text, flags=re.IGNORECASE)
    return text

def split_paragraph(text, max_len=300):
    sentences = re.split(r'(?<=[.?!])\s+', text)
    parts = []
    buf = ""
    for s in sentences:
        if len(buf) + len(s) < max_len:
            buf += " " + s if buf else s
        else:
            parts.append(buf)
            buf = s
    if buf:
        parts.append(buf)
    return parts

def semantic_enhance_answer(law_items):
    """
    Tách nội dung theo số thứ tự/khóa khoản và tạo block riêng
    """
    answer_blocks = []
    for d in law_items:
        content = highlight_keyphrases(d["noi_dung"], d.get("keyphrase", []))
        # Tách theo số thứ tự (ví dụ: 15., 16., ...)
        parts = re.split(r'(\d+\.)', content)
        buf = ""
        for i, part in enumerate(parts):
            if re.match(r'\d+\.', part):
                # Nếu buffer có nội dung, lưu block trước
                if buf.strip():
                    answer_blocks.append({
                        "title": f"{d['chuong']}, Điều {d['dieu']}",
                        "content": buf.strip(),
                        "source": d.get("source", "Luật Đất Đai")
                    })
                buf = part  # bắt đầu buffer mới
            else:
                buf += part
        if buf.strip():
            answer_blocks.append({
                "title": f"{d['chuong']}, Điều {d['dieu']}",
                "content": buf.strip(),
                "source": d.get("source", "Luật Đất Đai")
            })
    return answer_blocks

def answer_question(user_id, question, law_corpus=None):
    history = conversation_history.get(user_id, [])

    # ----- 1. Fuzzy search -----
    if law_corpus:
        fuzzy = fuzzy_search(question, law_corpus)
        fuzzy = [d for d in fuzzy if d["noi_dung"] not in history]
        if fuzzy:
            d = fuzzy[0]
            history.append(question)
            conversation_history[user_id] = history
            return semantic_enhance_answer([d]), []

    # ----- 2. Keyphrase search -----
    kp_results = search_by_keyphrase(question)
    kp_results = [d for d in kp_results if d["noi_dung"] not in history]
    if kp_results:
        item = kp_results[0]
        related = get_related_questions(question)
        history.append(question)
        conversation_history[user_id] = history
        return semantic_enhance_answer([item]), related

    # ----- 3. Semantic search -----
    sem = search_semantic(question, top_k=3)
    sem = [d for d in sem if d.get("score",0)>=0.3 and d["noi_dung"] not in history]
    if sem:
        seen = set()
        unique_docs = []
        for d in sem:
            if d["noi_dung"] not in seen:
                seen.add(d["noi_dung"])
                unique_docs.append(d)
        enhanced = semantic_enhance_answer(unique_docs)
        related = [d["noi_dung"] for d in unique_docs[1:]]
        history.append(question)
        conversation_history[user_id] = history
        return enhanced, related

    history.append(question)
    conversation_history[user_id] = history
    return [{"title":"Không tìm thấy","content":"Không tìm thấy nội dung phù hợp trong luật.","source":""}], []

def learn_from_feedback(question, answer_text, user_id="anonymous"):
    save_feedback(question, answer_text, user=user_id)
