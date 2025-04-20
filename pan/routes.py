from flask import request, jsonify
from .services import search_pan_resources
from functools import lru_cache
from time import time

# 简单的限流机制
last_request_time = 0
MIN_REQUEST_INTERVAL = 2  # 2秒间隔

def init_pan_routes(app):
    """优化后的API路由逻辑，增加缓存和限流"""
    @app.route('/api/search')
    def api_search():
        global last_request_time
        
        # 限流检查
        current_time = time()
        if current_time - last_request_time < MIN_REQUEST_INTERVAL:
            return jsonify({
                "error": "请求过于频繁，请稍后再试",
                "retry_after": MIN_REQUEST_INTERVAL - (current_time - last_request_time)
            }), 429
        last_request_time = current_time
        
        keyword = request.args.get('q', '').strip()
        if not keyword:
            return jsonify({"error": "关键词不能为空"}), 400
        
        try:
            results = search_pan_resources(keyword)['ysxjjkl']
            return jsonify({
                "success": True,
                "count": len(results),
                "results": results,
                "cached": False
            })
        except Exception as e:
            return jsonify({
                "error": "搜索服务暂时不可用",
                "details": str(e)
            }), 500