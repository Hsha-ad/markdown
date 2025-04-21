# pan/datasources.py
import requests
from bs4 import BeautifulSoup
import jieba

def search_douban(keyword):
    url = f"https://search.douban.com/movie/subject_search?search_text={keyword}"
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3'}
    try:
        response = requests.get(url, headers=headers)
        soup = BeautifulSoup(response.text, 'html.parser')
        results = []
        items = soup.select('.item-root')
        for item in items:
            title = item.select_one('.title a').text.strip()
            results.append(title)
        return results
    except Exception as e:
        print(f"[豆瓣搜索出错] {str(e)}")
        return []

def search_baidu(keyword):
    url = f"https://www.baidu.com/s?wd={keyword}"
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3'}
    try:
        response = requests.get(url, headers=headers)
        soup = BeautifulSoup(response.text, 'html.parser')
        results = []
        # 这里需要根据百度搜索结果的 HTML 结构进行调整
        return results
    except Exception as e:
        print(f"[百度搜索出错] {str(e)}")
        return []

def search_bing(keyword):
    url = f"https://www.bing.com/search?q={keyword}"
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3'}
    try:
        response = requests.get(url, headers=headers)
        soup = BeautifulSoup(response.text, 'html.parser')
        results = []
        # 这里需要根据必应搜索结果的 HTML 结构进行调整
        return results
    except Exception as e:
        print(f"[必应搜索出错] {str(e)}")
        return []

def get_movie_names(keyword):
    words = jieba.lcut(keyword)
    combinations = []
    for i in range(1, len(words) + 1):
        for j in range(len(words) - i + 1):
            combinations.append(''.join(words[j:j + i]))

    movie_names = set()
    for comb in combinations:
        movie_names.update(search_douban(comb))
        movie_names.update(search_baidu(comb))
        movie_names.update(search_bing(comb))

    return list(movie_names)