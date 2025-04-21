import requests
from bs4 import BeautifulSoup
import re
import time

def crawl_douban_celebrity_movies(celebrity_id):
    url = f"https://movie.douban.com/celebrity/{celebrity_id}/movies?sortby=time"
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
    }
    try:
        response = requests.get(url, headers=headers)
        response.raise_for_status()
        soup = BeautifulSoup(response.text, 'html.parser')
        movie_titles = []
        movie_items = soup.select('div.item')
        for item in movie_items:
            title_tag = item.select_one('span.title')
            if title_tag:
                title = title_tag.text.strip()
                movie_titles.append(title)
        return movie_titles
    except requests.RequestException as e:
        print(f"Error fetching Douban movies: {e}")
        return []
    except Exception as e:
        print(f"Unexpected error in crawl_douban_celebrity_movies: {e}")
        return []

def crawl_bing_movie_search(keyword):
    url = f"https://cn.bing.com/search?q={keyword}&form=ANNTH1"
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
    }
    try:
        response = requests.get(url, headers=headers)
        response.raise_for_status()
        soup = BeautifulSoup(response.text, 'html.parser')
        movie_titles = []
        text_content = soup.get_text()
        matches = re.findall(r'《(.*?)》', text_content)
        for match in matches:
            movie_titles.append(match)
        return movie_titles
    except requests.RequestException as e:
        print(f"Error fetching Bing search results: {e}")
        return []
    except Exception as e:
        print(f"Unexpected error in crawl_bing_movie_search: {e}")
        return []
    