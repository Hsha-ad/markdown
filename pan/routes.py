# pan/routes.py
from flask import request, jsonify
from .services import search_pan_resources

def init_pan_routes(app):
    """原封不动迁移您的API路由逻辑"""
    @app.route('/api/search')
    def api_search():
        keyword = request.args.get('q', '').strip()
        if not keyword:
            return jsonify({"error": "关键词不能为空"}), 400
        
        results = search_pan_resources(keyword)['ysxjjkl']
        return jsonify({
            "success": True,
            "count": len(results),
            "results": results
        })