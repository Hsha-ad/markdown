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

        chatInput.value = '';
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
        return data.results.map(item => {
            // 处理文件名过长的情况
            const maxLength = 20; // 最大长度
            let title = item.title;
            if (title.length > maxLength) {
                title = title.slice(0, maxLength) + '...';
            }

            return `
                <div class="result-card">
                    <div class="result-card-header">
                        <div class="result-card-title">🎬 《${title}》</div>
                        <div class="result-card-rating">★ 8.8/10 (豆瓣)</div>
                    </div>
                    <div class="result-card-poster" style="background-image: url('https://via.placeholder.com/100x150')"></div>
                    <div class="result-card-info">
                        <div class="result-card-row">
                            <div class="result-card-label">导演:</div>
                            <div class="result-card-value">克里斯托弗·诺兰</div>
                        </div>
                        <div class="result-card-row">
                            <div class="result-card-label">📅 上映日期:</div>
                            <div class="result-card-value">2023-08-30</div>
                        </div>
                        <div class="result-card-row">
                            <div class="result-card-label">🕒 片长:</div>
                            <div class="result-card-value">180 分钟</div>
                        </div>
                    </div>
                    <div class="result-card-radar">
                        <div class="result-card-row">
                            <div class="result-card-label">画质</div>
                            <div class="result-card-value">▰▰▰▰▰</div>
                            <div class="result-card-label">速度</div>
                            <div class="result-card-value">▰▰▰▱▱</div>
                        </div>
                        <div class="result-card-row">
                            <div class="result-card-label">字幕</div>
                            <div class="result-card-value">▰▰▰▰▱</div>
                            <div class="result-card-label">稳定</div>
                            <div class="result-card-value">▰▰▰▰▱</div>
                        </div>
                    </div>
                    <div class="result-card-resource">
                        <h4>🟢 在线观看</h4>
                        <ul>
                            <li>▪️ Netflix (需VPN)</li>
                            <li>▪️ 腾讯视频 (VIP专享)</li>
                        </ul>
                        <h4>🟠 网盘资源</h4>
                        <ul>
                            <li>▪️ 阿里云 (密码:6x8h) 4K HDR</li>
                        </ul>
                    </div>
                </div>
            `;
        }).join('');
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