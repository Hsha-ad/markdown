async function performSearch() {
    try {
        showLoading();
        
        // 添加请求超时控制
        const controller = new AbortController();
        const timeoutId = setTimeout(() => controller.abort(), 10000);
        
        const response = await fetch('/api/search', {
            method: 'POST',
            signal: controller.signal,
            headers: {
                'Content-Type': 'application/json',
                'X-Request-ID': generateRequestId()
            },
            body: JSON.stringify({ keyword: input.value.trim() })
        });
        
        clearTimeout(timeoutId);
        
        if (!response.ok) {
            throw new Error(`HTTP error! status: ${response.status}`);
        }
        
        const data = await response.json();
        if (data.error) {
            showError(data.error);
        } else {
            displayResults(data.data || []);
        }
    } catch (error) {
        showError(error.message.includes('abort') ? 
            '请求超时，请重试' : 
            '网络异常，请检查连接');
    } finally {
        hideLoading();
    }
}