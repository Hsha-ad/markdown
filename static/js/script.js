// 使用立即执行函数隔离作用域
(function() {
    // 全局变量声明（只声明一次）
    let chatInput, sendButton, chatContainer;

    // DOM加载完成后初始化
    document.addEventListener('DOMContentLoaded', function() {
        // 获取DOM元素
        chatInput = document.getElementById('chat-input');
        sendButton = document.getElementById('send-button');
        chatContainer = document.getElementById('chat-container');

        // 事件监听（确保元素存在）
        if (sendButton && chatInput) {
            sendButton.addEventListener('click', handleSendMessage);
            chatInput.addEventListener('keypress', function(e) {
                if (e.key === 'Enter') handleSendMessage();
            });
        }

        // 初始化滚动条
        scrollToBottom();
    });

    // 消息处理函数
    function handleSendMessage() {
        const keyword = chatInput.value.trim();
        if (!keyword) return;

        addUserMessage(keyword);
        chatInput.value = '';

        const typingElement = showTyping();
        
        fetch(`/api/search?q=${encodeURIComponent(keyword)}`)
            .then(response => response.json())
            .then(data => {
                chatContainer.removeChild(typingElement);
                addBotMessage(processSearchResults(data));
            })
            .catch(error => {
                console.error('搜索失败:', error);
                chatContainer.removeChild(typingElement);
                addBotMessage(`<p style="color:red">请求失败: ${error.message}</p>`);
            });
    }

    // 其他工具函数（保持原有功能）
    function addUserMessage(text) {
        const messageDiv = document.createElement('div');
        messageDiv.className = 'message user-message';
        messageDiv.innerHTML = `
            <img src="https://via.placeholder.com/40/95EC69/FFFFFF?text=You" class="avatar">
            <div class="message-content">
                <div class="nickname">你</div>
                <div class="bubble user-bubble">${text}</div>
            </div>
        `;
        chatContainer.appendChild(messageDiv);
        scrollToBottom();
    }

    function addBotMessage(html) {
        const messageDiv = document.createElement('div');
        messageDiv.className = 'message bot-message';
        messageDiv.innerHTML = `
            <img src="https://via.placeholder.com/40/07C160/FFFFFF?text=Bot" class="avatar">
            <div class="message-content">
                <div class="nickname">网盘助手</div>
                <div class="bubble bot-bubble">${html}</div>
            </div>
        `;
        chatContainer.appendChild(messageDiv);
        scrollToBottom();
    }

    function showTyping() {
        const typingDiv = document.createElement('div');
        typingDiv.className = 'message bot-message';
        typingDiv.innerHTML = `
            <img src="https://via.placeholder.com/40/07C160/FFFFFF?text=Bot" class="avatar">
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

    function processSearchResults(data) {
        if (!data.results || data.results.length === 0) {
            return '<p>没有找到相关资源</p>';
        }
        return data.results.map(item => `
            <div class="result-item">
                <div class="result-title">${item.title} 
                    <small>来自 ${item.source}</small>
                </div>
                <div class="link-box">
                    <input type="text" value="${item.url}" readonly>
                    <button onclick="copyLink(this)">复制</button>
                </div>
            </div>
        `).join('');
    }

    function scrollToBottom() {
        if (chatContainer) chatContainer.scrollTop = chatContainer.scrollHeight;
    }

    // 暴露全局函数（解决第三方脚本冲突）
    window.copyLink = function(button) {
        const input = button.parentElement.querySelector('input');
        input.select();
        document.execCommand('copy');
        button.textContent = '已复制';
        setTimeout(() => button.textContent = '复制', 2000);
    };
})();