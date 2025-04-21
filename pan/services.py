from .crawlers.ysxjjkl import search_ysxjjkl
from .datasources import get_movie_names
import logging

# 配置日志
logging.basicConfig(level=logging.ERROR)
logger = logging.getLogger(__name__)

def search_pan_resources(keyword):
    try:
        movie_names = get_movie_names(keyword)
        all_results = []
        for name in movie_names:
            results = search_ysxjjkl(name)
            all_results.extend(results)
        return {
            'ysxjjkl': all_results
        }
    except Exception as e:
        logger.error(f"[服务出错] {str(e)}", exc_info=True)
        return {'ysxjjkl': []}