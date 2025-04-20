document.addEventListener('DOMContentLoaded', function() {
    const searchBtn = document.getElementById('search-btn');
    const input = document.getElementById('search-input');
    const resultsContainer = document.getElementById('results');

    searchBtn.addEventListener('click', performSearch);
    input.addEventListener('keypress', function(e) {
        if (e.key === 'Enter') performSearch();
    });

    async function performSearch() {
        const keyword = input.value.trim();
        if (!keyword) return;

        showLoading();
        
        try {
            const response = await fetch('/api/search', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify({ keyword })
            });
            
            const data = await response.json();
            if (response.ok) {
                displayResults(data.data);
            } else {
                showError(data.error || '搜索失败');
            }
        } catch (error) {
            showError('网络请求异常');
        } finally {
            hideLoading();
        }
    }

    function displayResults(items) {
        resultsContainer.innerHTML = '';
        
        items.forEach(item => {
            if (item.type === 'title') {
                const titleEl = document.createElement('div');
                titleEl.className = 'result-title';
                titleEl.textContent = item.text;
                resultsContainer.appendChild(titleEl);
            } else {
                const itemEl = document.createElement('div');
                itemEl.className = 'result-item';
                
                const titleEl = document.createElement('div');
                titleEl.className = 'item-title';
                titleEl.textContent = item.title;
                
                const linkEl = document.createElement('div');
                linkEl.className = 'item-link';
                linkEl.innerHTML = `链接：<a href="${item.link}" target="_blank">${item.link}</a>`;
                
                const pwdEl = document.createElement('div');
                pwdEl.className = 'item-pwd';
                pwdEl.textContent = `提取码：${item.pwd}`;
                
                const copyBtn = document.createElement('button');
                copyBtn.className = 'copy-btn';
                copyBtn.textContent = '复制链接';
                copyBtn.onclick = () => copyToClipboard(item.link);
                
                itemEl.append(titleEl, linkEl, pwdEl, copyBtn);
                resultsContainer.appendChild(itemEl);
            }
        });
    }

    // 辅助函数保持不变...
});