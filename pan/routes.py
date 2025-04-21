from flask import Blueprint, request, jsonify
import requests
from bs4 import BeautifulSoup
from pan.crawlers.ysxjjkl import search_pan_resources

pan_bp = Blueprint('pan', __name__)

def search_bing(keyword):
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3'}
    url = f'https://cn.bing.com/search?q={keyword}'
    try:
        response = requests.get(url, headers=headers)
        response.raise_for_status()
        soup = BeautifulSoup(response.text, 'html.parser')
        movie_titles = []
        # 这里需要根据必应搜索结果的 HTML 结构调整选择器
        for title in soup.find_all('h2'):
            movie_titles.append(title.get_text().strip())
        return movie_titles
    except requests.RequestException as e:
        print(f"Error searching Bing: {e}")
        return []

@pan_bp.route('/search', methods=['GET'])
def search():
    keyword = request.args.get('keyword')
    if not keyword:
        return jsonify({"error": "Keyword is required"}), 400
    # 在必应搜索影视片名
    movie_titles = search_bing(keyword)
    all_resources = []
    for title in movie_titles:
        # 在现有资源渠道搜索网盘资源
        resources = search_pan_resources(title)
        all_resources.extend(resources)
    return jsonify({"resources": all_resources})
    