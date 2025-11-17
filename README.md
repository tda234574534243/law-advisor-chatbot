Chatbot Luật Đất Đai
====================

Một chatbot tra cứu kiến thức pháp luật về Luật Đất Đai, xây dựng bằng Python, Flask, và sử dụng Sentence Transformers để tìm câu trả lời dựa trên keyphrase và semantic search. Hệ thống còn hỗ trợ feedback để học thêm câu hỏi mới từ người dùng.

---------------------------------------------------

Tính năng:

- Tra cứu câu hỏi về Luật Đất Đai.
- Gợi ý câu hỏi liên quan (semantic similarity).
- Highlight các keyphrase quan trọng trong câu trả lời.
- Feedback để thêm câu hỏi mới vào cơ sở dữ liệu.
- Lưu lịch sử hội thoại cho multi-turn conversation.

---------------------------------------------------
```bash
Cấu trúc project:
│   .gitignore
│   README.md
│   requirements.txt
│
├───backend
│   │   app.py
│   │   bot.py
│   │   database.py
│   │   search.py
│   
│   
│          
│           
│           
│
├───data
│       law_db.json
│       luat_dat_dai.json
│
└───frontend
        index.html
        main.js
        style.css
```
---------------------------------------------------

Yêu cầu:

- Python 3.10+
- pip packages:
  - flask
  - tinydb
  - torch
  - sentence-transformers

Cài đặt packages:

pip install flask tinydb torch sentence-transformers

---------------------------------------------------

Cách chạy project:

1. Chạy backend Flask:

cd backend
python app.py

2. Mở trình duyệt vào:

http://127.0.0.1:5000

---------------------------------------------------

Sử dụng Chatbot:

- Nhập câu hỏi vào input.
- Nhấn "Gửi".
- Chatbot sẽ trả lời, highlight keyphrase, và hiển thị câu hỏi liên quan.
- Nhấn "👍 Feedback" nếu muốn chatbot học câu trả lời mới.

---------------------------------------------------

Cập nhật dữ liệu / Feedback:

- Mọi feedback từ người dùng sẽ được lưu vào law_db.json.
- Embedding mới sẽ tự động cập nhật để trả lời câu hỏi tương lai chính xác hơn.

---------------------------------------------------

Lưu ý:

- Đây là phiên bản demo, không phải tư vấn pháp lý chính thức.
- Sử dụng trong môi trường development. Không dùng trực tiếp trong production.
- Nếu database rỗng, luat_dat_dai.json sẽ được load tự động.

---------------------------------------------------
