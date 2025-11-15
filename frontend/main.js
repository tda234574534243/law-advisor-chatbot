async function askQuestion() {
    const qInput = document.getElementById("question");
    const question = qInput.value.trim();
    if (!question) return;
    const resp = await fetch("/ask", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ question, user_id: "user1" })
    });
    const data = await resp.json();
    const chatbox = document.getElementById("chatbox");
    chatbox.innerHTML += `<p><b>Q:</b> ${escapeHtml(question)}</p>`;
    chatbox.innerHTML += `<p><b>A:</b> ${data.answer ? data.answer : 'Không có'}</p>`;
    if (data.related_questions && data.related_questions.length) {
        chatbox.innerHTML += `<p><i>Câu hỏi liên quan:</i></p>`;
        data.related_questions.forEach(q => { chatbox.innerHTML += `<p style="margin-left:20px">- ${escapeHtml(q)}</p>`; });
    }
    chatbox.innerHTML += `<p><button onclick="sendFeedback('${escapeJs(question)}', '${escapeJs(data.answer||'')}')">👍 Feedback</button></p>`;
    qInput.value = "";
    chatbox.scrollTop = chatbox.scrollHeight;
}

async function sendFeedback(question, answer) {
    await fetch("/feedback", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ question: question, answer: answer, user: "user1" })
    });
    alert("Cảm ơn! Feedback đã được ghi nhận (lưu vào feedback queue).");
}

function escapeHtml(s) {
    if (!s) return '';
    return s.replace(/&/g,'&amp;').replace(/</g,'&lt;').replace(/>/g,'&gt;').replace(/"/g,'&quot;');
}
function escapeJs(s) {
    if (!s) return '';
    return s.replace(/'/g,"\\'").replace(/"/g,'\\"').replace(/\n/g,'\\n');
}
