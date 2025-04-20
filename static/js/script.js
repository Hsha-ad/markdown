const chatInput = document.getElementById('chat-input');
const sendButton = document.getElementById('send-button');
const chatContainer = document.getElementById('chat-container');

// 添加用户消息
function addUserMessage(text) {
    const messageDiv = document.createElement('div');
    messageDiv.className = 'message user-message';
    messageDiv.innerHTML = `
        <img src="https://via.placeholder.com/40/95EC69/FFFFFF?text=You" class="avatar" alt="用户头像">
        <div class="message-content">
            <div class="nickname">你</div>
            <div class="bubble user-bubble">${text}</div>
        </div>
    `;
    chatContainer.appendChild(messageDiv);
    scrollToBottom();
}

// 添加机器人消息
function addBotMessage(html) {
    const messageDiv = document.createElement('div');
    messageDiv.className = 'message bot-message';
    messageDiv.innerHTML = `
        <img src="https://via.placeholder.com/40/07C160/FFFFFF?text=Bot" class="avatar" alt="助手头像">
        <div class="message-content">
            <div class="nickname">网盘助手</div>
            <div class="bubble bot-bubble">${html}</div>
        </div>
    `;
    chatContainer.appendChild(messageDiv);
    scrollToBottom();
}

// 显示正在输入状态
function showTyping() {
    const typingDiv = document.createElement('div');
    typingDiv.className = 'message bot-message';
    typingDiv.innerHTML = `
        <img src="https://via.placeholder.com/40/07C160/FFFFFF?text=Bot" class="avatar" alt="助手头像">
        <div class="message-content">
            <div class="nickname">网盘助手</div>
            <div class="bubble bot-bubble">
                <div class="typing-indicator">
                    <div class="typing-dot"></div>
                    <div class="typing-dot"></div>
                    <div class="typing-dot"></div>
                </div>
            </div>
        </div>
    `;
    chatContainer.appendChild(typingDiv);
    scrollToBottom();
    return typingDiv;
}

// 滚动到底部
function scrollToBottom() {
    chatContainer.scrollTop = chatContainer.scrollHeight;
}

// 处理搜索结果
function processSearchResults(data) {
    if (!data.results || data.results.length === 0) {
        return '<p>没有找到相关资源，请尝试其他关键词。</p>';
    }
    
    const validResults = data.results.filter(item => item.valid !== false);
    if (validResults.length === 0) {
        return '<p>找到的资源链接已失效，请尝试其他关键词。</p>';
    }
    
    return validResults.map(item => `
        <div class="result-item">
            <div class="result-title">${item.title || '未命名资源'} 
                <small style="color: #888;">来自 ${item.source || '未知来源'}</small>
            </div>
            <div class="link-box">
                <input type="text" value="${item.url}" readonly>
                <button onclick="copyLink(this)">复制</button>
            </div>
        </div>
    `).join('');
}

// 复制链接
function copyLink(button) {
    const input = button.parentElement.querySelector('input');
    input.select();
    document.execCommand('copy');
    
    button.textContent = '已复制';
    setTimeout(() => {
        button.textContent = '复制';
    }, 2000);
}

// 发送搜索请求
async function sendSearchRequest(keyword) {
    try {
        const response = await fetch(`https://markdown-smoky-alpha.vercel.app/api/search?q=${encodeURIComponent(keyword)}`);
        
        if (!response.ok) {
            throw new Error(`请求失败: ${response.status}`);
        }
        
        const data = await response.json();
        return processSearchResults(data);
        
    } catch (error) {
        console.error('搜索出错:', error);
        return `<p>搜索失败: ${error.message}</p>`;
    }
}

// 处理发送消息
async function handleSendMessage() {
    const keyword = chatInput.value.trim();
    if (!keyword) return;
    
    // 添加用户消息
    addUserMessage(keyword);
    chatInput.value = '';
    
    // 显示机器人正在输入
    const typingElement = showTyping();
    
    // 发送请求并获取结果
    const resultHtml = await sendSearchRequest(keyword);
    
    // 移除正在输入状态
    chatContainer.removeChild(typingElement);
    
    // 添加机器人回复
    addBotMessage(resultHtml);
}

// 事件监听
sendButton.addEventListener('click', handleSendMessage);
chatInput.addEventListener('keypress', (e) => {
    if (e.key === 'Enter') handleSendMessage();
});