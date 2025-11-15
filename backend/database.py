# backend/database.py
import os
import json
from search import model, refresh_index
from sentence_transformers import util

DATA_DIR = os.path.join(os.path.dirname(__file__), "..", "data")
os.makedirs(DATA_DIR, exist_ok=True)

LAW_DB = os.path.join(DATA_DIR, "law_db.json")
FEEDBACK_DB = os.path.join(DATA_DIR, "feedback.json")

def load_data():
    """Load law_db và tạo feedback rỗng nếu chưa có"""
    if not os.path.exists(LAW_DB):
        raise FileNotFoundError("law_db.json missing. Run backend/reset_db.py to create baseline.")
    if not os.path.exists(FEEDBACK_DB):
        with open(FEEDBACK_DB, "w", encoding="utf-8") as f:
            json.dump([], f, ensure_ascii=False, indent=2)
    refresh_index()

def get_law_docs():
    with open(LAW_DB, "r", encoding="utf-8") as f:
        try:
            return json.load(f)
        except json.JSONDecodeError:
            return []

def save_law_docs(docs):
    with open(LAW_DB, "w", encoding="utf-8") as f:
        json.dump(docs, f, ensure_ascii=False, indent=2)
    refresh_index()

def save_feedback(question, answer_text, user="anonymous"):
    with open(FEEDBACK_DB, "r", encoding="utf-8") as f:
        try:
            arr = json.load(f)
        except json.JSONDecodeError:
            arr = []
    arr.append({
        "question": question,
        "answer": answer_text,
        "user": user
    })
    with open(FEEDBACK_DB, "w", encoding="utf-8") as f:
        json.dump(arr, f, ensure_ascii=False, indent=2)

def list_feedback():
    with open(FEEDBACK_DB, "r", encoding="utf-8") as f:
        try:
            return json.load(f)
        except json.JSONDecodeError:
            return []

def promote_feedback(index):
    feedback_list = list_feedback()
    if index < 0 or index >= len(feedback_list):
        raise IndexError("Invalid feedback index")
    item = feedback_list[index]

    docs = get_law_docs()
    new_emb = model.encode([item["answer"]], convert_to_tensor=True)
    for d in docs:
        existing_emb = model.encode([d.get("noi_dung", "")], convert_to_tensor=True)
        sim = util.cos_sim(new_emb, existing_emb).item()
        if sim > 0.92:
            return False, "Similar existing doc, not promoted."

    new_doc = {
        "chuong": "Chưa phân loại",
        "ten_chuong": "Feedback promoted",
        "dieu": len(docs) + 1,
        "noi_dung": item["answer"],
        "keyphrase": item["question"].lower().split()[:6]
    }
    docs.append(new_doc)
    save_law_docs(docs)

    # Xóa feedback đã promote
    feedback_list.pop(index)
    with open(FEEDBACK_DB, "w", encoding="utf-8") as f:
        json.dump(feedback_list, f, ensure_ascii=False, indent=2)

    return True, "Promoted"
