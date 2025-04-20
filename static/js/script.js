(function () {
    const chatMessages = document.getElementById('chat-messages');
    const userInput = document.getElementById('user-input');
    const sendButton = document.getElementById('send-button');
    let currentResultsData = [];
    let currentResultsPage = 1;
    const resultsPerPage = 5;

    function addUserMessage(message) {
        const userMessage = document.createElement('div');
        userMessage.classList.add('message', 'user-message');
        userMessage.innerHTML = `<div class="message-content"><p>${message}</p></div>`;
        chatMessages.appendChild(userMessage);
        scrollToBottom();
    }

    function addBotMessage(message) {
        const botMessage = document.createElement('div');
        botMessage.classList.add('message', 'bot-message');
        botMessage.innerHTML = `<div class="message-content">${message}</div>`;
        chatMessages.appendChild(botMessage);
        scrollToBottom();
    }

    function showTyping() {
        const typingMessage = document.createElement('div');
        typingMessage.classList.add('message', 'bot-message', 'typing-message');
        typingMessage.innerHTML = `<div class="message-content"><p><span class="typing-indicator"><span class="typing-dot"></span><span class="typing-dot"></span><span class="typing-dot"></span></p></div>`;
        chatMessages.appendChild(typingMessage);
        scrollToBottom();
    }

    function hideTyping() {
        const typingMessage = document.querySelector('.typing-message');
        if (typingMessage) {
            typingMessage.remove();
        }
    }

    function handleSendMessage() {
        const message = userInput.value.trim();
        if (message) {
            addUserMessage(message);
            showTyping();
            userInput.value = '';

            fetch(`/api/search?keyword=${encodeURIComponent(message)}`)
              .then(response => response.json())
              .then(data => {
                    hideTyping();
                    currentResultsData = data.results;
                    currentResultsPage = 1;
                    const resultsHtml = renderPaginatedResults();
                    addBotMessage(resultsHtml);
                })
              .catch(error => {
                    hideTyping();
                    addBotMessage('<p>请求出错，请稍后重试。</p>');
                    console.error('请求出错:', error);
                });
        }
    }

    function processSearchResults(data) {
        if (!data.results || data.results.length === 0) {
            return '<p>没有找到相关资源</p>';
        }
        return data.results.map(item => {
            const maxTitleLength = 30;
            let title = item.title;
            if (title.length > maxTitleLength) {
                title = title.slice(0, maxTitleLength) + '...';
            }
            let 网盘名称 = '未知网盘';
            if (item.url.includes('pan.baidu.com')) {
                网盘名称 = '百度网盘';
            } else if (item.url.includes('aliyundrive.com')) {
                网盘名称 = '阿里网盘';
            }
            return `
                <div class="result-item">
                    <div class="result-title">${title}</div>
                    <div class="button-group">
                        <button class="copy-link-button" onclick="copyLink('${item.url}')">复制链接</button>
                        <button class="open-in-app-button" onclick="openInApp('${item.url}')">${网盘名称}</button>
                    </div>
                </div>
            `;
        }).join('');
    }

    function renderPaginatedResults() {
        const start = (currentResultsPage - 1) * resultsPerPage;
        const end = start + resultsPerPage;
        const pageResults = currentResultsData.slice(start, end);
        const totalPages = Math.ceil(currentResultsData.length / resultsPerPage);

        const resultsHtml = processSearchResults({ results: pageResults });

        const paginationHtml = `
            <div class="pagination-controls">
                <button class="pagination-btn" onclick="changeResultsPage(-1)" ${currentResultsPage <= 1 ? 'disabled' : ''}>
                    上一页
                </button>
                <button class="pagination-btn" onclick="changeResultsPage(1)" ${end >= currentResultsData.length ? 'disabled' : ''}>
                    下一页
                </button>
            </div>
            <div class="pagination-info">
                第 ${currentResultsPage}/${totalPages} 页 (共 ${currentResultsData.length} 条结果)
            </div>
        `;

        return resultsHtml + paginationHtml;
    }

    function changeResultsPage(delta) {
        currentResultsPage += delta;
        const resultsHtml = renderPaginatedResults();
        const botMessage = document.querySelector('.bot-message:last-child .message-content');
        botMessage.innerHTML = resultsHtml;
        scrollToBottom();
    }

    function scrollToBottom() {
        chatMessages.scrollTop = chatMessages.scrollHeight;
    }

    function copyLink(link) {
        const tempInput = document.createElement('input');
        tempInput.value = link;
        document.body.appendChild(tempInput);
        tempInput.select();
        document.execCommand('copy');
        document.body.removeChild(tempInput);
        alert('链接已复制到剪贴板');
    }

    function openInApp(link) {
        window.open(link, '_blank');
    }

    sendButton.addEventListener('click', handleSendMessage);
    userInput.addEventListener('keydown', event => {
        if (event.key === 'Enter') {
            handleSendMessage();
        }
    });
})();
