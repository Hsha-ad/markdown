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

  function processSearchResults(data) {
    console.log('传入 processSearchResults 的数据:', data);
    if (!data || data.length === 0) {
        return '<p>没有找到相关资源</p>';
    }
    return data.map(item => {
        const maxLength = 20;
        let title = item.title;
        if (title.length > maxLength) {
            title = title.slice(0, maxLength) + '...';
        }

        // 解析网盘链接和密码
        let panLink = item.url;
        let pwd = '';
        if (panLink.includes('?pwd=')) {
            pwd = panLink.split('?pwd=')[1];
        }

        let panType = '未知网盘';
        if (panLink.includes('pan.baidu.com')) {
            panType = '百度网盘';
        } else if (panLink.includes('aliyundrive.com')) {
            panType = '阿里云盘';
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
                        <div class="result-card-value">暂无信息</div>
                    </div>
                    <div class="result-card-row">
                        <div class="result-card-label">📅 上映日期:</div>
                        <div class="result-card-value">暂无信息</div>
                    </div>
                    <div class="result-card-row">
                        <div class="result-card-label">🕒 片长:</div>
                        <div class="result-card-value">暂无信息</div>
                    </div>
                </div>
                <div class="result-card-radar">
                    <div class="result-card-row">
                        <div class="result-card-label">画质</div>
                        <div class="result-card-value">暂无信息</div>
                        <div class="result-card-label">速度</div>
                        <div class="result-card-value">暂无信息</div>
                    </div>
                    <div class="result-card-row">
                        <div class="result-card-label">字幕</div>
                        <div class="result-card-value">暂无信息</div>
                        <div class="result-card-label">稳定</div>
                        <div class="result-card-value">暂无信息</div>
                    </div>
                </div>
                <div class="result-card-resource">
                    <h4>🟠 网盘资源</h4>
                    <ul>
                        <li>▪️ ${panType} (密码:${pwd})</li>
                    </ul>
                </div>
            </div>
        `;
    }).join('');
}
