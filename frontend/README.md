📌 Frontend – Chatbot Luật Đất Đai
Giao diện web đơn giản cho phép người dùng đặt câu hỏi liên quan đến Luật Đất Đai, gửi yêu cầu đến backend Flask, nhận câu trả lời và hiển thị các đoạn luật được highlight màu sắc.
Frontend được phát triển hoàn toàn bằng HTML + CSS + JavaScript thuần, không sử dụng bất kỳ framework nào.
________________________________________
🚀 Tính năng
•	Giao diện chat đơn giản, dễ dùng
•	Gửi câu hỏi tới API /ask
•	Hiển thị câu trả lời từ backend (hỗ trợ HTML highlight)
•	Gợi ý các câu hỏi liên quan
•	Gửi phản hồi người dùng qua API /feedback
•	Tự động cuộn xuống tin nhắn mới nhất

________________________________________
🖼️ 1. index.html
Nhiệm vụ:
•	Tạo khung giao diện chatbot
•	Tạo ô nhập câu hỏi
•	Tạo nút gửi
•	Import file JavaScript chính main.js
Frontend được backend Flask serve thông qua:
<script src="/static/main.js"></script>
Điều này yêu cầu backend cấu hình:
static_folder = "../frontend"
________________________________________
🧠 2. main.js
File này xử lý toàn bộ logic giao tiếp giữa frontend và backend.
✔ Gửi câu hỏi đến backend
fetch("/ask", {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ question, user_id: "user1" })
});
✔ Hiển thị câu trả lời có highlight (không escape)
Backend trả về HTML để highlight điều luật → không escape:
chatbox.innerHTML += `<p class="answer"><b>A:</b> ${data.answer}</p>`;
✔ Hiển thị các câu hỏi liên quan
data.related_questions.forEach(q => {
    chatbox.innerHTML += `<p style="margin-left:20px">- ${escapeHtml(q)}</p>`;
});
✔ Gửi feedback từ người dùng
fetch("/feedback", {
    method: "POST",
    body: JSON.stringify({ question, answer, user: "user1" })
});
✔ Hàm escape chống XSS
Chỉ áp dụng cho input người dùng nhập, không áp dụng cho câu trả lời từ backend.
________________________________________
🎨 3. style.css
Điểm nổi bật:
•	Khung chat có viền + scroll
•	Câu trả lời có nền xanh nhạt tạo sự tách biệt
•	Highlight điều luật dùng class:
.law-highlight {
    color: #1565c0;
    font-weight: bold;
}
________________________________________
🔌 Cách chạy frontend
Frontend không cần server riêng, vì Flask sẽ serve toàn bộ file tĩnh.
Chạy backend:
cd backend
python app.py
Sau đó mở trình duyệt:
👉 http://localhost:5000/
index.html trong thư mục frontend sẽ tự động được tải lên.
________________________________________
🔧 API mà frontend sử dụng
POST /ask
Gửi câu hỏi → backend trả về câu trả lời + câu hỏi liên quan:
{
  "answer": "… giải thích từ luật …",
  "related_questions": ["…", "…"]
}
________________________________________
POST /feedback
Gửi câu hỏi + câu trả lời → backend lưu vào feedback queue.
{
  "question": "...",
  "answer": "...",
  "user": "user1"
}

