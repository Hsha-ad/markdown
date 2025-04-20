from flask import Flask, send_from_directory
import os

app = Flask(__name__, static_folder='static')

# 必须添加静态文件路由
@app.route('/static/<path:path>')
def serve_static(path):
    return send_from_directory('static', path)

# 核心API端点（与图片1功能严格对应）
@app.route('/api/search', methods=['POST'])
def search():
    from pan.services import SearchService
    service = SearchService()
    
    try:
        data = request.get_json()
        keyword = data.get('keyword', '')
        
        # 严格校验输入（防止Vercel崩溃）
        if not keyword or len(keyword) > 50:
            return {'error': 'Invalid keyword'}, 400
            
        # 执行图片1所示的多级搜索
        results = service.search_resources(keyword)
        return {
            'data': {
                'exact': results['exact_matches'],
                'related': results['related_content'],
                'short_plays': results['short_plays']
            }
        }
    except Exception as e:
        return {'error': str(e)}, 500

# 必须添加根路由
@app.route('/')
def index():
    return send_from_directory('templates', 'index.html')

if __name__ == '__main__':
    app.run()
