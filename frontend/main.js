async function askQuestion() {
    const question = document.getElementById("question").value.trim();
    if (!question) return;

    const response = await fetch("http://127.0.0.1:5000/ask", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ question, user_id: "user1" })
    });
    const data = await response.json();
    const chatbox = document.getElementById("chatbox");

    // Hiển thị câu hỏi
    const qElem = document.createElement("p");
    qElem.innerHTML = `<b>Q:</b> ${question}`;
    chatbox.appendChild(qElem);

    // Hiển thị câu trả lời
    const aElem = document.createElement("p");
    aElem.innerHTML = `<b>A:</b> ${data.answer}`;
    chatbox.appendChild(aElem);

    // Tạo nút feedback an toàn
    const btn = document.createElement("button");
    btn.textContent = "👍 Feedback";
    btn.dataset.question = question;
    btn.dataset.answer = data.answer;
    btn.addEventListener("click", async (e) => {
        await sendFeedback(e.target.dataset.question, e.target.dataset.answer);
    });
    chatbox.appendChild(btn);

    // Hiển thị câu hỏi liên quan
    if (data.related_questions && data.related_questions.length) {
        const relTitle = document.createElement("p");
        relTitle.innerHTML = `<i>Câu hỏi liên quan:</i>`;
        chatbox.appendChild(relTitle);

        data.related_questions.forEach(q => {
            const qRel = document.createElement("p");
            qRel.style.marginLeft = "20px";
            qRel.textContent = `- ${q}`;
            chatbox.appendChild(qRel);
        });
    }

    // Scroll xuống dưới
    chatbox.scrollTop = chatbox.scrollHeight;

    document.getElementById("question").value = "";
}

async function sendFeedback(question, answer) {
    try {
        const response = await fetch("http://127.0.0.1:5000/feedback", {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({ question, answer })
        });
        const data = await response.json();
        if (data.status === "success") {
            alert("Cảm ơn! Chatbot đã học từ feedback của bạn.");
        } else {
            alert("Lỗi khi gửi feedback: " + (data.error || "Unknown error"));
        }
    } catch (err) {
        alert("Lỗi network: " + err);
    }
}
