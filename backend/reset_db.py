# backend/reset_db.py
import json
import os

ROOT = os.path.join(os.path.dirname(__file__), "..")
DATA_DIR = os.path.join(ROOT, "data")
os.makedirs(DATA_DIR, exist_ok=True)
OUT = os.path.join(DATA_DIR, "law_db.json")
FEED = os.path.join(DATA_DIR, "feedback.json")

base = [
    {
      "chuong": "Chương I",
      "ten_chuong": "Những quy định chung",
      "dieu": 1,
      "noi_dung": "Phạm vi điều chỉnh và đối tượng áp dụng của Luật Đất đai.",
      "keyphrase": ["phạm vi điều chỉnh", "đối tượng áp dụng"]
    },
    {
      "chuong": "Chương II",
      "ten_chuong": "Quyền sử dụng đất",
      "dieu": 5,
      "noi_dung": "Người sử dụng đất có quyền chuyển nhượng, cho thuê, thừa kế quyền sử dụng đất.",
      "keyphrase": ["quyền sử dụng đất", "chuyển nhượng", "cho thuê", "thừa kế"]
    },
    {
      "chuong": "Chương III",
      "ten_chuong": "Trách nhiệm sử dụng đất",
      "dieu": 10,
      "noi_dung": "Người sử dụng đất phải sử dụng đất đúng mục đích, bảo vệ đất và thực hiện nghĩa vụ tài chính.",
      "keyphrase": ["sử dụng đất đúng mục đích", "nghĩa vụ tài chính"]
    }
]

with open(OUT, "w", encoding="utf-8") as f:
    json.dump(base, f, ensure_ascii=False, indent=2)

with open(FEED, "w", encoding="utf-8") as f:
    json.dump([], f, ensure_ascii=False, indent=2)

print(f"Reset done -> {OUT}")
print(f"Feedback cleared -> {FEED}")
