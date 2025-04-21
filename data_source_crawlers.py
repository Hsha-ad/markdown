import requests
from bs4 import BeautifulSoup
import re


def crawl_douban_celebrity_movies(celebrity_id):
    url = f"https://movie.douban.com/celebrity/{celebrity_id}/movies?sortby=time"
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3"}
    try:
        response = requests.get(url, headers=headers)
        response.raise_for_status()
        soup = BeautifulSoup(response.text, 'html.parser')
        movie_titles = []
        movie_items = soup.select('div.article > div > div > a')
        for item in movie_items:
            title = item.get('title')
            if title:
                movie_titles.append(title)
        return movie_titles
    except requests.RequestException as e:
        print(f"Error fetching data from Douban: {e}")
        return []


def crawl_bing_movie_search(keyword):
    url = f"https://cn.bing.com/search?q={keyword}&form=ANNTH1"
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3"}
    try:
        response = requests.get(url, headers=headers)
        response.raise_for_status()
        movie_titles = []
        pattern = re.compile(r'《(.*?)》')
        matches = pattern.findall(response.text)
        for match in matches:
            movie_titles.append(match)
        return movie_titles
    except requests.RequestException as e:
        print(f"Error fetching data from Bing: {e}")
        return []

    