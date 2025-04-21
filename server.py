# server.py
from flask import Flask, send_from_directory, request, jsonify
from pan.routes import init_pan_routes
import requests
from bs4 import BeautifulSoup

app = Flask(__name__, static_folder='static')

# 初始化网盘路由
init_pan_routes(app)

# 静态文件路由（原功能不变）
@app.route('/')
def serve_index():
    return send_from_directory('static', 'index.html')

@app.route('/<path:path>')
def serve_static(path):
    return send_from_directory('static', path)

@app.route('/api/search')
def api_search():
    keyword = request.args.get('q', '').strip()
    if not keyword:
        return jsonify({"error": "关键词不能为空"}), 400

    # 在必应搜索
    bing_results = search_bing(keyword)
    movie_titles = extract_movie_titles(bing_results)

    all_results = []
    from pan.crawlers.ysxjjkl import search_ysxjjkl
    for title in movie_titles:
        results = search_ysxjjkl(title)
        all_results.extend(results)

    return jsonify({
        "success": True,
        "count": len(all_results),
        "results": all_results
    })

def search_bing(keyword):
    url = f"https://www.bing.com/search?q={keyword}"
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3'}
    response = requests.get(url, headers=headers)
    return response.text

def extract_movie_titles(html):
    soup = BeautifulSoup(html, 'html.parser')
    titles = []
    # 这里简单假设标题在 <h2> 标签中，实际情况可能需要调整
    for h2 in soup.find_all('h2'):
        titles.append(h2.get_text())
    return titles

if __name__ == '__main__':
    app.run(port=5000)