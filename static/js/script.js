async function sendSearchRequest(keyword) {
    try {
        // 添加请求超时和重试机制
        const controller = new AbortController();
        const timeoutId = setTimeout(() => controller.abort(), 10000);
        
        const response = await fetch(`/api/search?q=${encodeURIComponent(keyword)}`, {
            signal: controller.signal,
            headers: {
                'Accept': 'application/json',
                'X-Requested-With': 'XMLHttpRequest'
            },
            credentials: 'include' // 确保携带cookie
        });
        
        clearTimeout(timeoutId);
        
        // 检查响应状态
        if (!response.ok) {
            throw new Error(`请求失败: ${response.status} ${response.statusText}`);
        }
        
        // 验证响应类型
        const contentType = response.headers.get('content-type');
        if (!contentType || !contentType.includes('application/json')) {
            const text = await response.text();
            if (text.startsWith('<!DOCTYPE html>')) {
                throw new Error('服务器返回了HTML页面，可能未登录或请求被拦截');
            }
            throw new Error('无效的JSON响应');
        }
        
        return await response.json();
        
    } catch (error) {
        console.error('搜索请求失败:', error);
        throw error; // 将错误传递给上层处理
    }
}
