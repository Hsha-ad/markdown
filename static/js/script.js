(function() {
    let chatInput, sendButton, resultContainer, pagination;
    let currentPage = 0;
    let allResults = [];

    document.addEventListener('DOMContentLoaded', function() {
        chatInput = document.getElementById('chat-input');
        sendButton = document.getElementById('send-button');
        resultContainer = document.getElementById('result-container');
        pagination = document.getElementById('pagination');

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

        fetch(`/api/search?q=${encodeURIComponent(keyword)}`)
           .then(response => response.json())
           .then(data => {
                allResults = data.results;
                currentPage = 0;
                showResults();
            })
           .catch(error => {
                console.error('搜索失败:', error);
                resultContainer.innerHTML = `<p style="color:red">请求失败: ${error.message}</p>`;
            });

        chatInput.value = '';
    }

   function showResults() {
    resultContainer.innerHTML = '';
    pagination.innerHTML = '';

    if (allResults.length === 0) {
        resultContainer.innerHTML = '<p>没有找到相关资源</p>';
        return;
    }

    const currentResult = allResults[currentPage];
    console.log('当前要显示的结果:', currentResult); // 添加日志
    const card = document.createElement('div');
    card.classList.add('result-card', 'active');
    card.innerHTML = processSearchResults([currentResult]);
    resultContainer.appendChild(card);

    if (allResults.length > 1) {
        const prevButton = document.createElement('button');
        prevButton.textContent = '←';
        prevButton.addEventListener('click', () => {
            if (currentPage > 0) {
                currentPage--;
                showResults();
            }
        });
        pagination.appendChild(prevButton);

        const nextButton = document.createElement('button');
        nextButton.textContent = '→';
        nextButton.addEventListener('click', () => {
            if (currentPage < allResults.length - 1) {
                currentPage++;
                showResults();
            }
        });
        pagination.appendChild(nextButton);
    }
}

    function processSearchResults(data) {
        if (!data || data.length === 0) {
            return '<p>没有找到相关资源</p>';
        }
        return data.map(item => {
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
})();
