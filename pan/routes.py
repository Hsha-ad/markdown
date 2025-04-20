from flask import request, jsonify
from .crawlers.ysxjjkl import search_ysxjjkl
import time

def init_pan_routes(app):
    @app.route('/api/search')
    def api_search():
        start_time = time.time()
        keyword = request.args.get('q', '').strip()
        if not keyword:
            return jsonify({"error": "关键词不能为空"}), 400
        
        try:
            results = search_ysxjjkl(keyword)
            elapsed = time.time() - start_time
            
            response = {
                "success": True,
                "keyword": keyword,
                "count": len(results),
                "results": results,
                "time": f"{elapsed:.2f}秒"
            }
            
            # 调试信息
            if not results:
                response['debug'] = {
                    "message": "没有找到结果，请检查爬虫解析逻辑",
                    "suggestion": "查看生成的debug_page.html分析页面结构"
                }
            
            return jsonify(response)
            
        except Exception as e:
            return jsonify({
                "error": "搜索服务暂时不可用",
                "details": str(e),
                "keyword": keyword
            }), 500