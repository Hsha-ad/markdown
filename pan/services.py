# pan/services.py
from .crawlers.ysxjjkl import search_ysxjjkl
from .datasources import get_movie_names

def search_pan_resources(keyword):
    """统一调用所有网盘爬虫（目前只有影视集结号）"""
    movie_names = get_movie_names(keyword)
    all_results = []
    for name in movie_names:
        results = search_ysxjjkl(name)
        all_results.extend(results)
    return {
        'ysxjjkl': all_results
    }