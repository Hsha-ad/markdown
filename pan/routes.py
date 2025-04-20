# pan/routes.py 修改版
from flask import Blueprint, request, jsonify
from .services import SearchService

bp = Blueprint('api', __name__)
service = SearchService()  # 使用改造后的服务

@bp.route('/search', methods=['POST'])
def search():
    data = request.get_json()
    keyword = data.get('keyword', '').strip()
    
    # 输入验证
    if not keyword or len(keyword) > 50:
        return jsonify({'error': '无效关键词'}), 400
        
    try:
        # 获取分类结果
        results = service.search_resources(keyword)
        if 'error' in results:
            return jsonify(results), 500
            
        # 按目标站格式返回
        return jsonify({
            'exact': results.get('exact_matches', []),
            'related': results.get('related', []),
            'short_plays': results.get('short_plays', [])
        })
    except Exception as e:
        return jsonify({'error': '服务器异常'}), 500