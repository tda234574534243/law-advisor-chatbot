# backend/bot.py
from search import search_by_keyphrase, search_semantic, get_related_questions
from database import save_feedback
import html
import re

conversation_history = {}

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

# ===== Main QA – KHÔNG LLM =====
def answer_question(user_id, question, law_corpus=None):
    history = conversation_history.get(user_id, [])

    # ===== 1. Keyphrase search =====
    kp = search_by_keyphrase(question)
    if kp:
        item = kp[0]
        content = highlight_keyphrases(item["noi_dung"], item.get("keyphrase", []))
        answer = f"{item['chuong']}, Điều {item['dieu']}: {content}"
        related = get_related_questions(question)
        history.append(question)
        conversation_history[user_id] = history
        return answer, related

    # ===== 2. Semantic search (top-1) =====
    sem = search_semantic(question, top_k=1)
    if sem:
        item = sem[0]
        answer = f"{item['chuong']}, Điều {item['dieu']}: {item['noi_dung']}"
        related = get_related_questions(question)
        history.append(question)
        conversation_history[user_id] = history
        return answer, related

    # ===== 3. fallback =====
    history.append(question)
    conversation_history[user_id] = history
    return "Không tìm thấy nội dung phù hợp trong luật.", []

# ===== Feedback =====
def learn_from_feedback(question, answer_text, user_id="anonymous"):
    save_feedback(question, answer_text, user=user_id)
