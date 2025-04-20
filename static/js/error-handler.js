// 错误隔离沙箱
window.addEventListener('error', function(e) {
    // 拦截第三方脚本错误
    if (e.filename.includes('all.js')) {
        e.preventDefault();
        console.warn('已阻止第三方脚本错误:', e.message);
        return false;
    }
    
    // 处理主程序错误
    console.error('系统错误:', e.error);
    document.getElementById('chat-container').innerHTML += `
        <div class="message bot-message">
            <div class="bubble bot-bubble" style="color:red">
                系统错误: ${e.message}
            </div>
        </div>
    `;
    return true;
});

// 防止未处理的Promise错误
window.addEventListener('unhandledrejection', function(e) {
    console.error('未处理的异步错误:', e.reason);
    e.preventDefault();
});