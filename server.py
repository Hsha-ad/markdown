# server.py
from flask import Flask, send_from_directory, request, jsonify
from pan.routes import init_pan_routes
import asyncio
import aiohttp
from bs4 import BeautifulSoup
import logging

app = Flask(__name__, static_folder='static')

# 配置日志
logging.basicConfig(level=logging.ERROR)

# 初始化网盘路由
init_pan_routes(app)

# 静态文件路由（原功能不变）
@app.route('/')
def serve_index():
    try:
        return send_from_directory('static', 'index.html')
    except Exception as e:
        logging.error(f"Error serving index.html: {e}")
        return jsonify({"error": "Internal server error"}), 500

@app.route('/<path:path>')
def serve_static(path):
    try:
        return send_from_directory('static', path)
    except Exception as e:
        logging.error(f"Error serving static file: {e}")
        return jsonify({"error": "Internal server error"}), 500

@app.route('/api/search')
async def api_search():
    try:
        keyword = request.args.get('q', '').strip()
        if not keyword:
            return jsonify({"error": "关键词不能为空"}), 400

        # 异步在必应搜索
        bing_results = await search_bing(keyword)
        movie_titles = extract_movie_titles(bing_results)

        all_results = []
        from pan.crawlers.ysxjjkl import search_ysxjjkl_async
        tasks = [search_ysxjjkl_async(title) for title in movie_titles]
        results_list = await asyncio.gather(*tasks)
        for results in results_list:
            all_results.extend(results)

        return jsonify({
            "success": True,
            "count": len(all_results),
            "results": all_results
        })
    except Exception as e:
        logging.error(f"Error in api_search: {e}")
        return jsonify({"error": "Internal server error"}), 500

async def search_bing(keyword):
    url = f"https://www.bing.com/search?q={keyword}"
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3'
    }
    async with aiohttp.ClientSession() as session:
        try:
            async with session.get(url, headers=headers) as response:
                return await response.text()
        except Exception as e:
            logging.error(f"Error in search_bing: {e}")
            return ""

def extract_movie_titles(html):
    soup = BeautifulSoup(html, 'html.parser')
    titles = []
    # 这里简单假设标题在 <h2> 标签中，实际情况可能需要调整
    for h2 in soup.find_all('h2'):
        titles.append(h2.get_text())
    return titles

if __name__ == '__main__':
    import asyncio
    asyncio.run(app.run(port=5000))