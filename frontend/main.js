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
    chatbox.innerHTML += `<p class="question"><b>Q:</b> ${escapeHtml(question)}</p>`;

    if (Array.isArray(data.answer)) {
        data.answer.forEach(block => {
            chatbox.innerHTML += `
                <div class="answer-block">
                    <div class="title" onclick="toggleBlock(this)">${escapeHtml(block.title)}</div>
                    <div class="content">${block.content}
                        <br><button class="feedback-btn" onclick="sendFeedback('${escapeJs(question)}', '${escapeJs(block.content)}')">👍 Gửi Feedback</button>
                    </div>
                </div>
            `;
        });
    } else {
        chatbox.innerHTML += `<p class="answer"><b>A:</b> ${escapeHtml(data.answer || 'Không có')}</p>`; 
    }

    if (data.related_questions && data.related_questions.length) {
        chatbox.innerHTML += `<p class="related"><i>Câu hỏi liên quan:</i></p>`;
        data.related_questions.forEach(q => {
            chatbox.innerHTML += `<p class="related" onclick="askRelated('${escapeJs(q)}')">- ${escapeHtml(q)}</p>`;
        });
    }

    qInput.value = "";
    chatbox.scrollTop = chatbox.scrollHeight;
}

function toggleBlock(el) {
    el.parentElement.classList.toggle("active");
}

async function askRelated(question) {
    document.getElementById("question").value = question;
    await askQuestion();
}

async function sendFeedback(question, answer) {
    await fetch("/feedback", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ question, answer, user: "user1" })
    });
    alert("Cảm ơn! Feedback đã được ghi nhận.");
}

function escapeHtml(s) {
    if (!s) return '';
    return s.replace(/&/g,'&amp;').replace(/</g,'&lt;').replace(/>/g,'&gt;').replace(/"/g,'&quot;');
}

function escapeJs(s) {
    if (!s) return '';
    return s.replace(/'/g,"\\'").replace(/"/g,'\\"').replace(/\n/g,'\\n');
}
