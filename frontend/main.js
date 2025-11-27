async function askQuestion() {
    const qInput = document.getElementById("question");
    const question = qInput.value.trim();
    if (!question) return;

    const chatArea = document.getElementById("chatArea");

    const welcomeContainer = document.querySelector('.welcome-container');
    if (welcomeContainer) {
        welcomeContainer.remove(); 
    }

    // Thêm câu hỏi người dùng
    const userMsg = document.createElement('div');
    userMsg.className = 'message user';
    userMsg.innerHTML = `<div class="message-content">${escapeHtml(question)}</div>`;
    chatArea.appendChild(userMsg);

    try {
        const mode = getSearchMode();
        const resp = await fetch("/query_auto", {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({ question, mode, user_id: "user1" })
        });
        const data = await resp.json();

        // Display AI response with typing animation
        if (Array.isArray(data.answer) && data.answer.length > 0) {
            data.answer.forEach(block => {
                const aiMsg = document.createElement('div');
                aiMsg.className = 'message ai';
                
                let content = `<strong>${escapeHtml(block.title || "Thông tin pháp lý")}</strong><br>`;
                
                if (block.reference) {
                    content += `<div class="reference-box">${escapeHtml(block.reference)}</div>`;
                }
                
                content += highlightKeyphrases(
                    block.content || 'Không có nội dung',
                    block.keyphrase || []
                );
                
                if (block.score) {
                    content += `<br><small>Độ tin cậy: ${(block.score * 100).toFixed(0)}%</small>`;
                }
                
                aiMsg.innerHTML = `<div class="message-content">${content}</div>`;
                chatArea.appendChild(aiMsg);
            });
        } else {
            const aiMsg = document.createElement('div');
            aiMsg.className = 'message ai';
            aiMsg.innerHTML = `<div class="message-content">${escapeHtml(data.answer || 'Không tìm thấy thông tin phù hợp.')}</div>`;
            chatArea.appendChild(aiMsg);
        }

        addToHistory(question);
    } catch (err) {
        console.error("Lỗi khi gọi API:", err);
        const errMsg = document.createElement('div');
        errMsg.className = 'message ai';
        errMsg.innerHTML = `<div class="message-content">Đã xảy ra lỗi. Vui lòng thử lại sau.</div>`;
        chatArea.appendChild(errMsg);
    }

    scrollToBottom();
}

// Scroll to bottom
function scrollToBottom() {
    const chatArea = document.getElementById("chatArea");
    chatArea.scrollTop = chatArea.scrollHeight;
}

// Suggested question
function askSuggested(text) {
    document.getElementById('question').value = text;
    askQuestion();
}

// Dark mode toggle
function toggleDarkMode() {
    document.body.classList.toggle('dark-mode');
    localStorage.setItem('darkMode', document.body.classList.contains('dark-mode'));
}

// New chat
function newChat() {
    document.getElementById('chatArea').innerHTML = `
        <div class="welcome-container">
            <div class="welcome-content">
                <h2 class="welcome-title">Xin chào! 👋</h2>
                <p class="welcome-subtitle">Tôi là trợ lý pháp lý chuyên tư vấn về <strong>Luật Đất đai 2013</strong></p>
                
                <div class="welcome-suggestions">
                    <p class="suggestions-title">Bạn có thể hỏi về:</p>
                    <div class="suggestion-grid">
                        <div class="suggestion-card" onclick="askSuggested('Nguyên tắc sử dụng đất là gì?')">
                            <span class="icon">📋</span>
                            <span>Nguyên tắc sử dụng đất</span>
                        </div>
                        <div class="suggestion-card" onclick="askSuggested('Thời hạn sử dụng đất nông nghiệp?')">
                            <span class="icon">🌾</span>
                            <span>Thời hạn sử dụng đất</span>
                        </div>
                        <div class="suggestion-card" onclick="askSuggested('Chuyển nhượng đất thủ tục gì?')">
                            <span class="icon">📝</span>
                            <span>Chuyển nhượng đất</span>
                        </div>
                        <div class="suggestion-card" onclick="askSuggested('Nhà nước thu hồi đất bồi thường thế nào?')">
                            <span class="icon">💰</span>
                            <span>Thu hồi & bồi thường</span>
                        </div>
                    </div>
                </div>
            </div>
        </div>
    `;
    document.getElementById('question').value = '';
    addToHistory('New Chat');
}

// Open settings
function openSettings() {
    alert('Cài đặt hiện chưa có. Vui lòng quay lại sau!');
}

// Chat history
function addToHistory(question) {
    const history = document.getElementById('chatHistory');
    const item = document.createElement('div');
    item.className = 'chat-history-item';
    item.textContent = question.substring(0, 50) + (question.length > 50 ? '...' : '');
    item.onclick = () => {
        document.getElementById('question').value = question;
        askQuestion();
    };
    history.insertBefore(item, history.firstChild);
}

// Handle input keypress
function handleInputKeyPress(event) {
    if (event.key === 'Enter' && !event.shiftKey) {
        event.preventDefault();
        askQuestion();
    }
}

function escapeHtml(text) {
    if (!text) return '';
    const div = document.createElement('div');
    div.textContent = text;
    return div.innerHTML;
}

// Get search mode from toggle
function getSearchMode() {
    const toggle = document.getElementById('searchModeToggle');
    return toggle.checked ? 'embedding' : 'tfidf';
}

// Highlight keyphrases
function highlightKeyphrases(text, keyphrases) {
    if (!keyphrases || keyphrases.length === 0) return escapeHtml(text);
    
    let result = escapeHtml(text);
    keyphrases.forEach(phrase => {
        const escaped = escapeRegex(phrase);
        const regex = new RegExp(`\\b${escaped}\\b`, 'gi');
        result = result.replace(regex, `<span class="keyphrase-highlight">$&</span>`);
    });
    return result;
}

// Escape regex special characters
function escapeRegex(str) {
    if (!str) return '';
    return str.replace(/[.*+?^${}()|[\]\\]/g, '\\$&');
}

// Load dark mode preference
if (localStorage.getItem('darkMode') === 'true') {
    document.body.classList.add('dark-mode');
}