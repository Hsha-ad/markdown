import requests
from bs4 import BeautifulSoup
import jieba
import logging

# 配置日志
logging.basicConfig(level=logging.ERROR)
logger = logging.getLogger(__name__)

def search_douban(keyword):
    url = f"https://search.douban.com/movie/subject_search?search_text={keyword}"
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3'}
    try:
        response = requests.get(url, headers=headers, timeout=5)
        response.raise_for_status()
        soup = BeautifulSoup(response.text, 'html.parser')
        results = []
        items = soup.select('.item-root')
        for item in items:
            title = item.select_one('.title a').text.strip()
            results.append(title)
        return results
    except requests.RequestException as e:
        logger.error(f"[豆瓣搜索出错] {str(e)}", exc_info=True)
        return []
    except Exception as e:
        logger.error(f"[豆瓣搜索未知错误] {str(e)}", exc_info=True)
        return []

def search_baidu(keyword):
    url = f"https://www.baidu.com/s?wd={keyword}"
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3'}
    try:
        response = requests.get(url, headers=headers, timeout=5)
        response.raise_for_status()
        soup = BeautifulSoup(response.text, 'html.parser')
        results = []
        return results
    except requests.RequestException as e:
        logger.error(f"[百度搜索出错] {str(e)}", exc_info=True)
        return []
    except Exception as e:
        logger.error(f"[百度搜索未知错误] {str(e)}", exc_info=True)
        return []

def search_bing(keyword):
    url = f"https://www.bing.com/search?q={keyword}"
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3'}
    try:
        response = requests.get(url, headers=headers, timeout=5)
        response.raise_for_status()
        soup = BeautifulSoup(response.text, 'html.parser')
        results = []
        return results
    except requests.RequestException as e:
        logger.error(f"[必应搜索出错] {str(e)}", exc_info=True)
        return []
    except Exception as e:
        logger.error(f"[必应搜索未知错误] {str(e)}", exc_info=True)
        return []

def get_movie_names(keyword):
    try:
        words = jieba.lcut(keyword)
        combinations = []
        for i in range(1, len(words) + 1):
            for j in range(len(words) - i + 1):
                combinations.append(''.join(words[j:j + i]))

        movie_names = set()
        for comb in combinations:
            douban_results = search_douban(comb)
            logger.info(f"豆瓣搜索 {comb} 结果: {douban_results}")
            movie_names.update(douban_results)
            baidu_results = search_baidu(comb)
            logger.info(f"百度搜索 {comb} 结果: {baidu_results}")
            movie_names.update(baidu_results)
            bing_results = search_bing(comb)
            logger.info(f"必应搜索 {comb} 结果: {bing_results}")
            movie_names.update(bing_results)

        return list(movie_names)
    except Exception as e:
        logger.error(f"[获取电影名称出错] {str(e)}", exc_info=True)
        return []