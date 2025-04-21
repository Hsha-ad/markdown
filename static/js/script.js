// 获取 DOM 元素
const chatContainer = document.getElementById('chat-container');
const inputField = document.getElementById('input-field');
const sendButton = document.getElementById('send-button');

// 添加用户消息到聊天容器
function addUserMessage(message) {
    const userMessage = document.createElement('div');
    userMessage.classList.add('user-message');
    userMessage.textContent = message;
    chatContainer.appendChild(userMessage);
    chatContainer.scrollTop = chatContainer.scrollHeight;
}

// 添加机器人消息到聊天容器
function addBotMessage(message) {
    const botMessage = document.createElement('div');
    botMessage.classList.add('bot-message');
    botMessage.innerHTML = message;
    chatContainer.appendChild(botMessage);
    chatContainer.scrollTop = chatContainer.scrollHeight;
}

// 显示加载提示
function showLoading() {
    const loadingMessage = document.createElement('div');
    loadingMessage.classList.add('bot-message');
    loadingMessage.textContent = '正在搜索，请稍候...';
    chatContainer.appendChild(loadingMessage);
    chatContainer.scrollTop = chatContainer.scrollHeight;
    return loadingMessage;
}

// 移除加载提示
function removeLoading(loadingMessage) {
    if (loadingMessage) {
        chatContainer.removeChild(loadingMessage);
    }
}

// 处理搜索请求
async function searchResources(keyword) {
    const loadingMessage = showLoading();
    try {
        const response = await fetch(`/pan/search?keyword=${encodeURIComponent(keyword)}`);
        if (!response.ok) {
            throw new Error('网络请求失败');
        }
        const data = await response.json();
        removeLoading(loadingMessage);
        if (data.resources.length === 0) {
            addBotMessage('未找到相关资源。');
        } else {
            let resultHtml = '<div class="search-results">';
            data.resources.forEach((resource) => {
                resultHtml += `
                    <div class="result-card">
                        <h3>${resource.title}</h3>
                        <p><strong>链接:</strong> <a href="${resource.link}" target="_blank">${resource.link}</a></p>
                        <p><strong>提取码:</strong> ${resource.extract_code}</p>
                    </div>
                `;
            });
            resultHtml += '</div>';
            addBotMessage(resultHtml);
        }
    } catch (error) {
        removeLoading(loadingMessage);
        addBotMessage(`发生错误: ${error.message}`);
    }
}

// 发送消息事件处理
function sendMessage() {
    const keyword = inputField.value.trim();
    if (keyword) {
        addUserMessage(keyword);
        searchResources(keyword);
        inputField.value = '';
    }
}

// 绑定事件
sendButton.addEventListener('click', sendMessage);
inputField.addEventListener('keydown', (event) => {
    if (event.key === 'Enter') {
        sendMessage();
    }
});

// 初始化欢迎消息
addBotMessage('欢迎使用网盘资源助手，请输入搜索关键词。');
    