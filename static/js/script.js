// static/js/script.js
document.addEventListener('DOMContentLoaded', function () {
    const chatInput = document.getElementById('chat-input');
    const sendButton = document.getElementById('send-button');
    const chatContainer = document.getElementById('chat-container');

    sendButton.addEventListener('click', function () {
        console.log('点击事件已触发');
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
                    console.log('后端返回的数据:', data);
                    if (data.success) {
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
