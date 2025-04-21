import requests
from bs4 import BeautifulSoup
import re
import time
import random

USER_AGENTS = [
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/109.0.0.0 Safari/537.36",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 13_2) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/109.0.0.0 Safari/537.36",
    "Mozilla/5.0 (iPhone; CPU iPhone OS 16_3 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/16.3 Mobile/15E148 Safari/604.1",
]

def crawl_douban_celebrity_movies(celebrity_id):
    url = f"https://movie.douban.com/celebrity/{celebrity_id}/movies?sortby=time"
    headers = {
        "User-Agent": random.choice(USER_AGENTS),
        "Accept-Language": "zh-CN,zh;q=0.9"
    }
    try:
        response = requests.get(url, headers=headers)
        response.raise_for_status()
        time.sleep(random.uniform(3, 5))
        soup = BeautifulSoup(response.text, 'html.parser')
        return [item.select_one('span.title').text.strip() 
                for item in soup.select('div.item') 
                if item.select_one('span.title')]
    except Exception as e:
        print(f"Douban crawl error: {e}")
        return []

def crawl_bing_movie_search(keyword):
    url = f"https://cn.bing.com/search?q={keyword}&form=ANNTH1"
    headers = {
        "User-Agent": random.choice(USER_AGENTS),
        "Accept-Language": "zh-CN,zh;q=0.9",
        "Referer": "https://cn.bing.com/"
    }
    try:
        response = requests.get(url, headers=headers, timeout=10)
        response.raise_for_status()
        time.sleep(random.uniform(3, 5))
        soup = BeautifulSoup(response.text, 'html.parser')
        text_content = soup.get_text()
        movies = re.findall(r'《(.*?)》', text_content)
        return [m for m in movies if not any(word in m for word in ["讨论", "分析", "内涵", "推荐"]) ]
    except Exception as e:
        print(f"Bing crawl error: {e}")
        return []