(function() {
    let chatInput, sendButton, resourceContainer;
    let currentIndex = 0;
    let searchResults = [];

    document.addEventListener('DOMContentLoaded', function() {
        chatInput = document.getElementById('chat-input');
        sendButton = document.getElementById('send-button');
        resourceContainer = document.getElementById('resource-container');

        if (sendButton && chatInput) {
            sendButton.addEventListener('click', handleSendMessage);
            chatInput.addEventListener('keypress', function(e) {
                if (e.key === 'Enter') handleSendMessage();
            });
        }
    });

    function handleSendMessage() {
        const keyword = chatInput.value.trim();
        if (!keyword) return;

        currentIndex = 0;
        resourceContainer.innerHTML = '';
        const loadingElement = showLoading();

        fetch(`/api/search?q=${encodeURIComponent(keyword)}`)
           .then(response => response.json())
           .then(data => {
                resourceContainer.removeChild(loadingElement);
                searchResults = data.results;
                if (searchResults.length > 0) {
                    showResultCard(searchResults[currentIndex]);
                    setupSwipe();
                } else {
                    resourceContainer.innerHTML = '<p>没有找到相关资源</p>';
                }
            })
           .catch(error => {
                console.error('搜索失败:', error);
                resourceContainer.removeChild(loadingElement);
                resourceContainer.innerHTML = `<p style="color:red">请求失败: ${error.message}</p>`;
            });

        chatInput.value = '';
    }

    function showLoading() {
        const loadingDiv = document.createElement('div');
        loadingDiv.textContent = '正在搜索，请稍候...';
        resourceContainer.appendChild(loadingDiv);
        return loadingDiv;
    }

    function showResultCard(result) {
        const maxLength = 20;
        let title = result.title;
        if (title.length > maxLength) {
            title = title.slice(0, maxLength) + '...';
        }

        const cardHtml = `
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
        resourceContainer.innerHTML = cardHtml;
    }

    function setupSwipe() {
        let startX = 0;
        let startY = 0;

        resourceContainer.addEventListener('touchstart', function(e) {
            startX = e.touches[0].clientX;
            startY = e.touches[0].clientY;
        });

        resourceContainer.addEventListener('touchend', function(e) {
            const endX = e.changedTouches[0].clientX;
            const endY = e.changedTouches[0].clientY;
            const dx = endX - startX;
            const dy = endY - startY;

            if (Math.abs(dx) > Math.abs(dy)) {
                if (dx > 50) {
                    // 右滑
                    if (currentIndex > 0) {
                        currentIndex--;
                        showResultCard(searchResults[currentIndex]);
                    }
                } else if (dx < -50) {
                    // 左滑
                    if (currentIndex < searchResults.length - 1) {
                        currentIndex++;
                        showResultCard(searchResults[currentIndex]);
                    }
                }
            } else {
                if (dy < -50) {
                    // 上滑
                    if (currentIndex < searchResults.length - 1) {
                        currentIndex++;
                        showResultCard(searchResults[currentIndex]);
                    }
                }
            }
        });
    }
})();