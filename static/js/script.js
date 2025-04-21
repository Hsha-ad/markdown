(function() {
    let chatInput, sendButton, chatContainer;

    document.addEventListener('DOMContentLoaded', function() {
        chatInput = document.getElementById('chat-input');
        sendButton = document.getElementById('send-button');
        chatContainer = document.getElementById('chat-container');

        if (sendButton && chatInput) {
            sendButton.addEventListener('click', handleSendMessage);
            chatInput.addEventListener('keypress', function(e) {
                if (e.key === 'Enter') handleSendMessage();
            });
        }

        scrollToBottom();
    });

    function handleSendMessage() {
        const keyword = chatInput.value.trim();
        if (!keyword) return;

        addUserMessage(keyword);
        const typingElement = showTyping();

        fetch(`/api/search?q=${encodeURIComponent(keyword)}`)
           .then(response => response.json())
           .then(data => {
                chatContainer.removeChild(typingElement);
                addBotMessage(processSearchResults(data));
                // 添加资源卡片动画
                const resultCards = document.querySelectorAll('.result-card');
                resultCards.forEach((card, index) => {
                    setTimeout(() => {
                        card.classList.add('show');
                    }, index * 200);
                });
            })
           .catch(error => {
                console.error('搜索失败:', error);
                chatContainer.removeChild(typingElement);
                addBotMessage(`<p style="color:red">请求失败: ${error.message}</p>`);
            });

        chatInput.value = '';
    }

    function addUserMessage(text) {
        const messageDiv = document.createElement('div');
        messageDiv.classList.add('message', 'user-message');
        messageDiv.textContent = text;
        chatContainer.appendChild(messageDiv);
        scrollToBottom();
    }

    function addBotMessage(html) {
        const messageDiv = document.createElement('div');
        messageDiv.innerHTML = html;
        chatContainer.appendChild(messageDiv);
        scrollToBottom();
    }

    function showTyping() {
        const typingDiv = document.createElement('div');
        typingDiv.classList.add('message', 'bot-message', 'typing');
        typingDiv.textContent = '正在搜索，请稍候...';
        chatContainer.appendChild(typingDiv);
        scrollToBottom();
        return typingDiv;
    }

    function processSearchResults(data) {
        if (!data.results || data.results.length === 0) {
            return '<p>没有找到相关资源</p>';
        }
        return data.results.map(item => {
            const maxLength = 20;
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

    window.copyLink = function(button) {
        const input = button.parentElement.querySelector('input');
        input.select();
        document.execCommand('copy');
        button.textContent = '已复制';
        setTimeout(() => button.textContent = '复制', 2000);
    };
})();