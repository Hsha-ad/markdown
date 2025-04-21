// static/js/script.js
document.addEventListener('DOMContentLoaded', function () {
    const chatInput = document.getElementById('chat-input');
    const sendButton = document.getElementById('send-button');
    const chatContainer = document.getElementById('chat-container');

    sendButton.addEventListener('click', function () {
        const keyword = chatInput.value.trim();
        if (keyword) {
            // 调用后端 API
            fetch(`/api/search?q=${encodeURIComponent(keyword)}`)
              .then(response => {
                    if (!response.ok) {
                        throw new Error(`HTTP error! status: ${response.status}`);
                    }
                    return response.json();
                })
              .then(data => {
                    if (data.success) {
                        if (data.count === 0) {
                            // 没有找到相关资源，显示提示消息
                            const noResultMessage = document.createElement('div');
                            noResultMessage.classList.add('message', 'bot-message');
                            noResultMessage.innerHTML = `
                                <div class="bubble bot-bubble" style="color:orange">
                                    未找到与 "${keyword}" 相关的资源，请尝试其他关键词。
                                </div>
                            `;
                            chatContainer.appendChild(noResultMessage);
                        } else {
                            // 显示搜索结果
                            const results = data.results;
                            results.forEach(result => {
                                const message = document.createElement('div');
                                message.classList.add('message', 'bot-message');
                                message.innerHTML = `
                                    <div class="bubble bot-bubble">
                                        ${result.title}: <a href="${result.url}" target="_blank">${result.url}</a>
                                    </div>
                                `;
                                chatContainer.appendChild(message);
                            });
                        }
                    } else {
                        // 显示错误信息
                        const errorMessage = document.createElement('div');
                        errorMessage.classList.add('message', 'bot-message');
                        errorMessage.innerHTML = `
                            <div class="bubble bot-bubble" style="color:red">
                                ${data.error}
                            </div>
                        `;
                        chatContainer.appendChild(errorMessage);
                    }
                })
              .catch(error => {
                    // 处理网络错误
                    const errorMessage = document.createElement('div');
                    errorMessage.classList.add('message', 'bot-message');
                    errorMessage.innerHTML = `
                        <div class="bubble bot-bubble" style="color:red">
                            网络错误: ${error.message}
                        </div>
                    `;
                    chatContainer.appendChild(errorMessage);
                });
        }
    });
});
