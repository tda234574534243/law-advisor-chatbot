
 🚀 Backend – Luật Đất Đai AI Assistant

Backend được xây dựng bằng Flask + Python, kết hợp SentenceTransformer, LLM (Qwen 1.8B) và cơ chế học từ phản hồi (feedback learning).
Hệ thống xử lý câu hỏi về luật đất đai bằng cách:

 Tìm kiếm theo keyphrase
 Fuzzy matching (RapidFuzz)
 Semantic search (Sentence-BERT)
 Nâng cao câu trả lời bằng LLM
 Tự động học từ phản hồi người dùng (feedback promotion)



 📌 1. Yêu cầu hệ thống

 Python 3.10+
 CUDA (không bắt buộc, nhưng có để tăng tốc)
 gói Python:

  ```
  Flask
  torch
  transformers
  sentence-transformers
  rapidfuzz
  ```
 Thư mục data/ phải chứa:

   `law_db.json` – database luật
   `feedback.json` – lưu phản hồi người dùng



 📌 2. Cách chạy backend

Cài dependencies

```bash
pip install -r requirements.txt
```

Khởi tạo database gốc

```bash
python backend/reset_db.py
```

Chạy backend

```bash
python backend/app.py
```

Backend chạy tại:

```
http://localhost:5000
```

Frontend sẽ được serve trực tiếp từ thư mục `frontend/`.



 📌 3. Chức năng chính

✅ Serve frontend

 Trả file `index.html` và toàn bộ static frontend.

✅ /ask – Trả lời câu hỏi luật

Xử lý theo pipeline:

1. Keyphrase search
2. Fuzzy matching
3. Semantic search (SBERT)
4. LLM enhancement (Qwen 1.8B)

Trả về:

```json
{
  "answer": "…",
  "related_questions": [...]
}
```



✅ /feedback – Nhận phản hồi người dùng

Lưu thông tin:

 câu hỏi
 câu trả lời
 người gửi

Dữ liệu dùng để học lại.



✅ /admin/feedback – Xem toàn bộ feedback

Admin có thể xem feedback để đánh giá câu trả lời máy học được.



✅ /admin/promote – Thêm phản hồi vào luật

Hoạt động:

 encode feedback
 so sánh similarity với luật hiện tại
 nếu khác biệt đủ lớn → thêm vào `law_db.json`
 nếu quá giống → từ chối

Trả về:

```json
{"ok": true, "msg": "..."}
```



 📌 4. Các thành phần quan trọng

🔹 bot.py

 Chứa logic trả lời câu hỏi
 Highlight keyphrase
 Gọi LLM để nâng chất lượng câu trả lời
 Quản lý lịch sử hội thoại theo `user_id`

Pipeline trả lời:

1. Keyphrase → chính xác, ưu tiên cao
2. Fuzzy → tương đồng 60%+
3. Semantic search → dùng SBERT
4. LLM enhance → giải thích dễ hiểu
5. Fallback → không tìm thấy gì



🔹 search.py

 Tải SentenceTransformer
 Tạo embedding index
 Keyphrase search
 Fuzzy search bằng RapidFuzz
 Semantic search (cosine similarity)
 Gợi ý câu hỏi liên quan



🔹 database.py

 Load/save `law_db.json`
 Lưu feedback
 Promote feedback thành luật chính thức
 Tạo lại embedding index khi dữ liệu thay đổi



🔹 reset_db.py

 Khởi tạo database mẫu
 Xóa feedback cũ



 📌 5. API Endpoints

| Method | Endpoint          | Mô tả                    |
| GET    | `/`               | Trả frontend             |
| POST   | `/ask`            | Trả lời câu hỏi luật     |
| POST   | `/feedback`       | Lưu phản hồi người dùng  |
| GET    | `/admin/feedback` | Danh sách phản hồi       |
| POST   | `/admin/promote`  | Thêm phản hồi thành luật |



 📌 6. Mô hình AI đang dùng

Semantic Search Model

 all-MiniLM-L6-v2 (SentenceTransformer)

LLM

 Qwen 1.5 – 1.8B Chat
 Dùng để:

   gộp nội dung luật
   diễn giải lại mượt mà, dễ hiểu
   tránh lặp theo lịch sử hội thoại

Fuzzy Search

 RapidFuzz – thích hợp cho tiếng Việt



 📌 7. Học từ phản hồi (Feedback Learning)

Quy trình:

1. Người dùng gửi feedback
2. Hệ thống lưu vào `feedback.json`
3. Admin xét duyệt
4. Hệ thống:

    Encode nội dung feedback
    So sánh với toàn bộ luật
    Nếu similarity < 0.85 → thêm thành luật mới
    Ngược lại từ chối (tránh trùng)

Tự động cải thiện theo thời gian.



 📌 8. Ghi chú triển khai

 Có thể bật GPU để tăng tốc embedding và LLM
 Nên deploy backend bằng Gunicorn hoặc Uvicorn + nginx
 Nếu triển khai trên VPS cần preload model trước để tránh load lâu



 📌 9. License

MIT 



