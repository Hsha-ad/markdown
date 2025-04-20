from flask import request, jsonify
from .crawlers.ysxjjkl import search_ysxjjkl

def init_pan_routes(app):
    @app.route('/api/search')
    def api_search():
        keyword = request.args.get('q', '').strip()
        if not keyword:
            return jsonify({"error": "关键词不能为空"}), 400
        
        try:
            # 直接使用爬虫返回的完整结果
            results = search_ysxjjkl(keyword)
            return jsonify({
                "success": True,
                "count": len(results),
                "results": results
            })
        except Exception as e:
            return jsonify({
                "error": "搜索服务暂时不可用",
                "details": str(e)
            }), 500
