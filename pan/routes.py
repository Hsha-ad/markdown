from flask import Blueprint, request, jsonify
from .crawlers.ysxjjkl import search_ysxjjkl
from ..data_source_crawlers import crawl_douban_celebrity_movies, crawl_bing_movie_search

pan_bp = Blueprint('pan', __name__)


@pan_bp.route('/api/search', methods=['GET'])
def search():
    keyword = request.args.get('keyword')
    if not keyword:
        return jsonify({"error": "Keyword is required"}), 400
    results = search_ysxjjkl(keyword)
    return jsonify({"results": results})


@pan_bp.route('/api/enhanced_search', methods=['GET'])
def enhanced_search():
    keyword = request.args.get('keyword')
    if not keyword:
        return jsonify({"error": "Keyword is required"}), 400

    # 假设这里可以根据关键词映射到豆瓣影人 ID，实际应用中可能需要更复杂的处理
    celebrity_id = None
    if "周星驰" in keyword:
        celebrity_id = "1048026"

    movie_titles = []
    if celebrity_id:
        movie_titles = crawl_douban_celebrity_movies(celebrity_id)
    if not movie_titles:
        movie_titles = crawl_bing_movie_search(keyword)

    pan_results = []
    for title in movie_titles:
        results = search_ysxjjkl(title)
        pan_results.extend(results)

    return jsonify({"results": pan_results})

    