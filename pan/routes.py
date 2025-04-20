from flask import jsonify
from werkzeug.middleware.proxy_fix import ProxyFix

app = Flask(__name__)
app.wsgi_app = ProxyFix(app.wsgi_app)

@app.route('/api/search', methods=['POST'])
def safe_search():
    try:
        # 请求参数验证
        data = request.get_json()
        if not data or 'keyword' not in data:
            return jsonify({'error': 'Invalid request'}), 400
        
        # 内存保护
        if len(data['keyword']) > 100:
            return jsonify({'error': 'Keyword too long'}), 413
            
        # 速率限制
        if not rate_limiter.check(request):
            return jsonify({'error': 'Too many requests'}), 429
            
        # 执行搜索
        result = crawler.safe_search(data['keyword'])
        return jsonify(result)
        
    except Exception as e:
        app.logger.error(f"Search failed: {str(e)}")
        return jsonify({'error': 'Internal error'}), 500