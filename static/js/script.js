function displayResults(data) {
    const container = document.getElementById('results');
    container.innerHTML = '';

    // 精确匹配区块
    if (data.exact && data.exact.length) {
        const header = document.createElement('h3');
        header.textContent = '🔍 精确匹配';
        container.appendChild(header);
        
        data.exact.forEach(item => {
            container.appendChild(createItemElement(item));
        });
    }

    // 短剧区块（完全匹配目标站样式）
    if (data.short_plays && data.short_plays.length) {
        const header = document.createElement('h3');
        header.textContent = '🎬 短剧资源';
        container.appendChild(header);
        
        data.short_plays.forEach(item => {
            const el = createItemElement(item);
            el.classList.add('short-play');  // 添加短剧专属样式
            container.appendChild(el);
        });
    }
    
    // 相关资源区块
    if (data.related && data.related.length) {
        const header = document.createElement('h3');
        header.textContent = '📚 相关资源';
        container.appendChild(header);
        
        data.related.forEach(item => {
            container.appendChild(createItemElement(item));
        });
    }
}