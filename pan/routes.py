from flask import Blueprint, request, jsonify
from pan.services import SearchService

bp = Blueprint('api', __name__)
service = SearchService()

@bp.route('/search', methods=['POST'])
def search():
    data = request.get_json()
    keyword = data.get('keyword', '').strip()
    
    if not keyword or len(keyword) > 50:
        return jsonify({'error': '无效关键词'}), 400
        
    try:
        results = service.get_formatted_results(keyword)
        return jsonify({'data': results})
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@bp.route('/health')
def health_check():
    return jsonify({'status': 'healthy'})