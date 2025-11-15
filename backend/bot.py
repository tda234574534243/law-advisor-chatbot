# file: backend/bot.py
from search import search_by_keyphrase, search_semantic, get_related_questions
from database import add_feedback

conversation_history = {}

def highlight_keyphrases(text, keyphrases):
    colors = ["#f44336", "#2196F3", "#4CAF50", "#FF9800"]
    for i, kp in enumerate(keyphrases):
        color = colors[i % len(colors)]
        text = text.replace(kp, f"<span style='color:{color};font-weight:bold'>{kp}</span>")
    return text

def answer_question(user_id, question):
    history = conversation_history.get(user_id, [])
    context = " ".join(history[-3:])
    combined_query = context + " " + question

    results = search_by_keyphrase(combined_query)
    if results:
        item = results[0]
    else:
        item = search_semantic(combined_query)

    if not item:
        return "Xin lỗi, không tìm thấy câu trả lời phù hợp.", []

    highlighted_text = highlight_keyphrases(item["noi_dung"], item.get("keyphrase", []))

    history.append(question)
    conversation_history[user_id] = history

    related = get_related_questions(question)

    answer_text = f"{item.get('chuong','')}, Điều {item.get('dieu','')}: {highlighted_text}"
    return answer_text, related

def learn_from_feedback(question, answer_text):
    add_feedback(question, answer_text)
