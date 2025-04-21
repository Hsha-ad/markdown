from flask import Flask, request, jsonify
from pan.routes import init_pan_routes
import asyncio
import aiohttp
from bs4 import BeautifulSoup
from flask_cors import CORS

app = Flask(__name__)
CORS(app)
init_pan_routes(app)

# 异步 Bing 搜索
async def async_search_bing(keyword):
    timeout = aiohttp.ClientTimeout(total=5)  # 5 秒超时
    async with aiohttp.ClientSession(timeout=timeout) as session:
        try:
            async with session.get(
                f"https://www.bing.com/search?q={keyword}",
                headers={'User-Agent': 'Mozilla/5.0'}
            ) as response:
                return await response.text()
        except Exception as e:
            print(f"Bing 搜索错误: {e}")
            return ""

# 提取标题（简化示例）
def extract_movie_titles(html):
    return [tag.text.strip() for tag in BeautifulSoup(html, 'lxml').find_all('h2')[:5]]  # 取前5条

# 异步 API 接口
@app.route('/api/search')
async def api_search():
    keyword = request.args.get('q', '').strip()
    if not keyword:
        return jsonify({"error": "关键词不能为空"}), 400

    # 执行异步搜索
    bing_html = await async_search_bing(keyword)
    titles = extract_movie_titles(bing_html)
    
    # 模拟异步爬虫（需根据实际爬虫修改）
    async def mock_crawler(title):
        await asyncio.sleep(1)  # 模拟延迟
        return [f"{title} - 网盘链接: https://example.com/{title}"]
    
    # 并发处理多个标题
    results = await asyncio.gather(*[mock_crawler(title) for title in titles])
    all_results = [item for sublist in results for item in sublist]
    
    return jsonify({
        "success": True,
        "count": len(all_results),
        "results": all_results[:10]  # 限制结果数量，避免超时
    })

if __name__ == '__main__':
    asyncio.run(app.run(port=5000))