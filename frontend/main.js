async function askQuestion() {
    const qInput = document.getElementById("question");
    const question = qInput.value.trim();
    if (!question) return;

    const chatbox = document.getElementById("chatbox");

    const welcomeSection = document.querySelector('.welcome-section');
    if (welcomeSection) {
        welcomeSection.remove(); 
    }


    document.querySelector('.chat-container').classList.add('has-content');

    // Thêm câu hỏi người dùng
    const qDiv = document.createElement('div');
    qDiv.className = 'question';
    qDiv.innerHTML = `<b>Q:</b> ${escapeHtml(question)}`;
    chatbox.appendChild(qDiv);

    try {
        const resp = await fetch("/ask", {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({ question, user_id: "user1" })
        });
        const data = await resp.json();

        // XỬ LÝ NHIỀU ĐIỀU LUẬT 
        if (Array.isArray(data.answer) && data.answer.length > 0) {
            data.answer.forEach(block => {
                const lawBlock = document.createElement('div');
                lawBlock.className = 'law-block';

                lawBlock.innerHTML = `
                    <div class="law-header" onclick="toggleLawBlock(this)">
                        <span>${escapeHtml(block.title || "Thông tin pháp lý")}</span>
                       <span class="arrow">&#9660</span>
                    </div>
                    <div class="law-content">
                        ${block.reference ? `<div class="law-ref">${escapeHtml(block.reference)}</div>` : ''}
                        <div class="law-text">${block.content || 'Không có nội dung'}</div>
                        <button class="feedback-btn" onclick="sendFeedback('${escapeJs(question)}','${escapeJs(block.content || "")}')">👍 Gửi Feedback</button>
                    </div>
                `;
                chatbox.appendChild(lawBlock);
            });
        } else {
            // Trường hợp trả lời dạng text đơn
            const aDiv = document.createElement('div');
            aDiv.className = 'answer';
            aDiv.innerHTML = `<b>A:</b> ${escapeHtml(data.answer || 'Không tìm thấy thông tin phù hợp.')}`;
            chatbox.appendChild(aDiv);
        }

        // CÂU HỎI GỢI Ý
        if (data.related_questions && data.related_questions.length > 0) {
            const relTitle = document.createElement('div');
            relTitle.className = 'related-title';
            relTitle.innerHTML = '<i>Câu hỏi liên quan:</i>';
            chatbox.appendChild(relTitle);

            data.related_questions.forEach(q => {
                const rel = document.createElement('div');
                rel.className = 'related';
                rel.textContent = `• ${q}`;
                rel.style.cursor = 'pointer';
                rel.onclick = () => askRelated(q);
                chatbox.appendChild(rel);
            });
        }

    } catch (err) {
        console.error("Lỗi khi gọi API:", err);
        const errDiv = document.createElement('div');
        errDiv.className = 'answer';
        errDiv.innerHTML = `<b>A:</b> Đã xảy ra lỗi. Vui lòng thử lại sau.`;
        chatbox.appendChild(errDiv);
    }

    qInput.value = "";
    scrollToBottom();
}

// CLICK ĐỂ MỞ/ĐÓNG ĐIỀU LUẬT
function toggleLawBlock(header) {
    const thisBlock = header.parentElement;
    const wasActive = thisBlock.classList.contains('active');

    // Đóng tất cả
    document.querySelectorAll('.law-block').forEach(b => b.classList.remove('active'));

    // Mở lại cái vừa click nếu chưa active
    if (!wasActive) {
        thisBlock.classList.add('active');
    }
}

// CLICK CÂU HỎI GỢI Ý
async function askRelated(question) {
    document.getElementById("question").value = question;
    await askQuestion();
}

// GỬI FEEDBACK
async function sendFeedback(question, answer) {
    try {
        await fetch("/feedback", {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({ question, answer, user: "user1" })
        });
        alert("Cảm ơn bạn! Feedback đã được gửi thành công.");
    } catch (err) {
        alert("Gửi feedback thất bại. Vui lòng thử lại.");
    }
}


function escapeHtml(text) {
    if (!text) return '';
    const div = document.createElement('div');
    div.textContent = text;
    return div.innerHTML;
}

function escapeJs(text) {
    if (!text) return '';
    return text.replace(/'/g, "\\'").replace(/"/g, '\\"').replace(/\n/g, '\\n');
}


function scrollToBottom() {
    const chatbox = document.getElementById("chatbox");
    chatbox.scrollTop = chatbox.scrollHeight;
}


function askSuggested(text) {
    document.getElementById('question').value = text;
    askQuestion();
}