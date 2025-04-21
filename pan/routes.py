from flask import Blueprint, request, jsonify
from pan.crawlers.ysxjjkl import search_ysxjjkl
from data_source_crawlers import crawl_douban_celebrity_movies, crawl_bing_movie_search

pan_bp = Blueprint('pan', __name__)


@pan_bp.route('/api/search', methods=['GET'])
def search():
    keyword = request.args.get('keyword')
    if not keyword:
        return jsonify({"error": "Keyword is required"}), 400

    # 假设这里可以根据关键词解析出豆瓣影人ID，这里简单模拟
    celebrity_id = None
    if "周星驰" in keyword:
        celebrity_id = "1048026"

    movie_titles = []
    if celebrity_id:
        movie_titles = crawl_douban_celebrity_movies(celebrity_id)
    if not movie_titles:
        movie_titles = crawl_bing_movie_search(keyword)

    all_results = []
    for title in movie_titles:
        results = search_ysxjjkl(title)
        all_results.extend(results)

    return jsonify({"results": all_results})
    