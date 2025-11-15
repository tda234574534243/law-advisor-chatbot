# file: backend/database.py
import json
import os
from tinydb import TinyDB
from search import model, embeddings

DB_PATH = "data/law_db.json"
DATA_PATH = "data/luat_dat_dai.json"

def load_data():
    os.makedirs(os.path.dirname(DB_PATH), exist_ok=True)
    db = TinyDB(DB_PATH)
    if len(db) == 0:
        # Nếu DB rỗng, load dữ liệu mặc định
        with open(DATA_PATH, "r", encoding="utf-8") as f:
            data = json.load(f)
        # Convert dict _default -> list
        if "_default" in data:
            data_list = [v for k,v in data["_default"].items()]
        else:
            data_list = data
        db.insert_multiple(data_list)

    # Tạo embeddings ban đầu
    global embeddings
    embeddings.clear()
    contents = [item["noi_dung"] for item in db.all()]
    if contents:
        embeddings.extend(model.encode(contents, convert_to_tensor=True))
    return db

def add_feedback(question, answer_text):
    db = TinyDB(DB_PATH)
    keyphrase = question.lower().split()[:5]
    new_item = {
        "chuong": "Chưa phân loại",
        "ten_chuong": "Feedback mới",
        "dieu": len(db.all()) + 1,
        "noi_dung": answer_text,
        "keyphrase": keyphrase
    }
    db.insert(new_item)

    # cập nhật embedding ngay lập tức
    global embeddings
    new_emb = model.encode([answer_text], convert_to_tensor=True)
    embeddings.append(new_emb[0])

