________________________________________
📌 Frontend – Chatbot Luật Đất Đai
Giao diện web đơn giản cho phép người dùng đặt câu hỏi về Luật Đất Đai, gửi yêu cầu đến backend Flask, nhận câu trả lời và hiển thị các đoạn luật được highlight.
Frontend được viết hoàn toàn bằng HTML + CSS + JavaScript thuần
________________________________________
🚀 Tính năng
•	Giao diện chat đơn giản, dễ dùng
•	Gửi câu hỏi tới API /ask
•	Hiển thị câu trả lời có highlight màu sắc (HTML từ backend)
•	Gợi ý các câu hỏi liên quan
•	Gửi phản hồi người dùng qua API /feedback
•	Tự động cuộn xuống tin nhắn mới nhất
________________________________________
📁 Các file trong thư mục frontend/
frontend/
├── index.html      # Giao diện chính
├── main.js         # Logic gửi câu hỏi và xử lý phản hồi
└── style.css       # Style giao diện
________________________________________
🖼️ 1. index.html
•	Tạo khung giao diện chatbot
•	Input để nhập câu hỏi
•	Nút gửi
•	Thẻ <script> import file main.js
Frontend được serve qua Flask:
<script src="/static/main.js"></script>
Nghĩa là backend phải dùng:
static_folder="../frontend"
________________________________________
🧠 2. main.js
File này xử lý toàn bộ logic giao tiếp:
✔ Gửi câu hỏi
Gọi API:
fetch("/ask", {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ question, user_id: "user1" })
});
✔ Hiển thị câu trả lời có highlight
Do backend trả về văn bản có HTML (gạch màu), nên không escape câu trả lời:
chatbox.innerHTML += `<p class="answer"><b>A:</b> ${data.answer}</p>`;
✔ Hiển thị câu hỏi liên quan
data.related_questions.forEach(q => {
    chatbox.innerHTML += `<p style="margin-left:20px">- ${escapeHtml(q)}</p>`;
});
✔ Gửi feedback
fetch("/feedback", {
    method: "POST",
    body: JSON.stringify({ question, answer, user: "user1" })
});
✔ Hàm escape để tránh XSS
Chỉ áp dụng cho input người dùng nhập.
________________________________________
🎨 3. style.css
Thiết kế đơn giản:
•	Khung chat có border, scrollable
•	Màu xanh nhẹ cho câu trả lời
•	Highlight luật bằng class .law-highlight
🔌 Cách chạy frontend
Vì frontend được serve bởi backend Flask, bạn không cần chạy server frontend riêng.
Chỉ cần:
cd backend
python app.py
Sau đó truy cập:
👉 http://localhost:5000/
index.html sẽ tự được tải lên từ thư mục frontend.
________________________________________
🔧 API mà frontend sử dụng
POST /ask
Gửi câu hỏi → trả về:
{
  "answer": "… giải thích từ luật …",
  "related_questions": ["…", "…"]
}
POST /feedback
Gửi câu hỏi + câu trả lời → lưu vào feedback queue.


