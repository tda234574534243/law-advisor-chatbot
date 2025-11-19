async function askQuestion() {
    const qInput = document.getElementById("question");
    const question = qInput.value.trim();
    if (!question) return;

    const chatbox = document.getElementById("chatbox");

    // Add user question
    const qDiv = document.createElement('p');
    qDiv.className = 'question';
    qDiv.innerHTML = `<b>Q:</b> ${escapeHtml(question)}`;
    chatbox.appendChild(qDiv);
    scrollToBottom();

    try {
        const resp = await fetch("/ask", {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({ question, user_id: "user1" })
        });
        const data = await resp.json();

        // Handle answer (luôn show, kể cả trống)
        if (Array.isArray(data.answer) && data.answer.length > 0) {
            data.answer.forEach(block => {
                const blockDiv = document.createElement('div');
                blockDiv.className = 'answer-block';
                blockDiv.innerHTML = `
                    <div class="title" onclick="toggleBlock(this)">${escapeHtml(block.title)}</div>
                    <div class="content">${block.content || 'Không có nội dung'}<br>
                        <button class="feedback-btn" onclick="sendFeedback('${escapeJs(question)}','${escapeJs(block.content || "")}')">👍 Gửi Feedback</button>
                    </div>
                `;
                chatbox.appendChild(blockDiv);
            });
        } else {
            const aDiv = document.createElement('p');
            aDiv.className = 'answer';
            aDiv.innerHTML = `<b>A:</b> ${escapeHtml(data.answer || 'Không có câu trả lời')} `;
            chatbox.appendChild(aDiv);
        }

        // Related questions
        if (data.related_questions && data.related_questions.length) {
            const relatedTitle = document.createElement('div');
            relatedTitle.innerHTML = `<b>Câu hỏi liên quan:</b>`;
            chatbox.appendChild(relatedTitle);

            data.related_questions.forEach(q => {
                const span = document.createElement('span');
                span.className = 'related';
                span.textContent = q;
                span.onclick = () => askRelated(q);
                chatbox.appendChild(span);
            });
        }
    } catch (err) {
        // Khi fetch lỗi hoặc backend trả lỗi
        const errDiv = document.createElement('p');
        errDiv.className = 'answer';
        errDiv.innerHTML = `<b>A:</b> Không thể trả lời.`;
        chatbox.appendChild(errDiv);
    }

    scrollToBottom();
    qInput.value = "";
}

// Toggle answer block
function toggleBlock(el) {
    el.parentElement.classList.toggle("active");
    scrollToBottom();
}

// Related question click
async function askRelated(question) {
    document.getElementById("question").value = question;
    await askQuestion();
}

// Feedback gửi
async function sendFeedback(question, answer) {
    await fetch("/feedback", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ question, answer, user: "user1" })
    });
    alert("Cảm ơn! Feedback đã được ghi nhận.");
}

// Escape html & js
function escapeHtml(s) {
    if (!s) return '';
    return s.replace(/&/g,'&amp;').replace(/</g,'&lt;').replace(/>/g,'&gt;').replace(/"/g,'&quot;');
}

function escapeJs(s) {
    if (!s) return '';
    return s.replace(/'/g,"\\'").replace(/"/g,'\\"').replace(/\n/g,'\\n');
}

// Scroll mượt xuống cuối
function scrollToBottom() {
    const chatbox = document.getElementById("chatbox");
    chatbox.scrollTop = chatbox.scrollHeight;
}
