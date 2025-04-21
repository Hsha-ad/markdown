from flask import request, jsonify
from .services import search_pan_resources

def init_pan_routes(app):
    @app.route('/api/search')
    def api_search():
        keyword = request.args.get('q', '').strip()
        if not keyword:
            return jsonify({"error": "关键词不能为空"}), 400
        try:
            results = search_pan_resources(keyword)['ysxjjkl']
            return jsonify({
                "success": True,
                "count": len(results),
                "results": results
            })
        except Exception as e:
            return jsonify({"error": f"搜索过程中出现错误: {str(e)}"}), 500