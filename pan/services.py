# pan/services.py
from .crawlers.ysxjjkl import search_ysxjjkl

def search_pan_resources(keyword):
    """统一调用所有网盘爬虫（目前只有影视集结号）"""
    return {
        'ysxjjkl': search_ysxjjkl(keyword)  # 保持原功能不变
    }