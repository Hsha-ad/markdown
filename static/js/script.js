// 修改为绝对路径请求（防止Vercel路由问题）
const API_ENDPOINT = window.location.origin + '/api/search';

async function performSearch() {
    try {
        const response = await fetch(API_ENDPOINT, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'X-Requested-With': 'XMLHttpRequest'  // 必须添加
            },
            body: JSON.stringify({
                keyword: document.getElementById('search-input').value
            })
        });
        
        if (!response.ok) {
            throw new Error(`HTTP error! status: ${response.status}`);
        }
        
        const data = await response.json();
        
        // 严格按图片1格式渲染
        renderResults({
            exact: data.data?.exact || [],
            related: data.data?.related || [],
            shortPlays: data.data?.short_plays || []
        });
        
    } catch (error) {
        console.error('Search failed:', error);
        showError(error.message);
    }
}

// 图片1的精确渲染逻辑
function renderResults(sections) {
    const container = document.getElementById('results');
    container.innerHTML = '';
    
    // 精确匹配区块
    if (sections.exact.length) {
        const header = createSectionHeader('🔍 精确匹配');
        container.appendChild(header);
        
        sections.exact.forEach(item => {
            container.appendChild(createResultItem(item));
        });
    }
    
    // 相关资源区块（与图片1完全一致）
    if (sections.related.length) {
        const header = createSectionHeader('📚 相关资源');
        container.appendChild(header);
        
        sections.related.forEach(item => {
            container.appendChild(createResultItem(item));
        });
    }
    
    // 短剧资源区块（图片1的[短剧]标签）
    if (sections.shortPlays.length) {
        const header = createSectionHeader('🎬 短剧资源');
        container.appendChild(header);
        
        sections.shortPlays.forEach(item => {
            const elem = createResultItem(item);
            elem.dataset.shortPlay = true;  // 添加短剧标记
            container.appendChild(elem);
        });
    }
}
