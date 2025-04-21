# pan/crawlers/ysxjjkl.py
import requests
from bs4 import BeautifulSoup
import re
import sys
from urllib.parse import quote
from difflib import SequenceMatcher
from core.utils import check_valid

def is_similar(a, b, threshold=0.6):
    """判断两个字符串是否相似"""
    return SequenceMatcher(None, a, b).ratio() >= threshold

def search_ysxjjkl(keyword):
    try:
        url = f"https://ysxjjkl.souyisou.top/?search={quote(keyword)}"
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36',
            'Referer': 'https://ysxjjkl.souyisou.top/',
            'X-Requested-With': 'XMLHttpRequest'
        }

        print(f"[新版爬虫] 请求URL: {url}", file=sys.stderr)
        response = requests.get(url, headers=headers, timeout=15)
        response.raise_for_status()

        soup = BeautifulSoup(response.text, 'html.parser')
        results = []

        for item in soup.select('.box'):
            try:
                # 提取标题
                info_div = item.find('div', class_='info')
                if info_div:
                    # 获取链接前面的文本内容作为标题
                    title = info_div.contents[0].strip()
                else:
                    title = "未命名资源"

                link = item.find('a', href=lambda x: x and ('pan.baidu.com' in x or 'aliyundrive.com' in x))
                if not link:
                    continue

                pwd = None
                pwd_text = info_div.get_text() if info_div else ""
                pwd_match = re.search(r'提取码：([a-zA-Z0-9]{4})', pwd_text)
                if pwd_match:
                    pwd = pwd_match.group(1)

                # 模糊匹配判断
                if is_similar(title.lower(), keyword.lower()):
                    result = {
                        'title': title[:100],
                        'url': link['href'],
                        'source': '影视集结号',
                        'valid': bool(pwd)
                    }

                    if pwd and 'pwd=' not in result['url']:
                        result['url'] += f"?pwd={pwd}" if '?' not in result['url'] else f"&pwd={pwd}"

                    results.append(result)

            except Exception as e:
                print(f"[解析异常] {str(e)}", file=sys.stderr)
                continue

        if not results:
            print("[警告] 主解析方案无结果，尝试备用方案", file=sys.stderr)
            for a in soup.find_all('a', href=re.compile(r'pan\.baidu\.com/s/[^\s]+')):
                title = a.get_text(strip=True) or "百度网盘资源"
                if is_similar(title.lower(), keyword.lower()):
                    results.append({
                        'title': title,
                        'url': a['href'],
                        'source': 'ysxjjkl',
                        'valid': 'pwd=' in a['href']
                    })

        print(f"[有效结果] 找到 {len(results)} 条资源", file=sys.stderr)
        return results

    except Exception as e:
        print(f"[爬虫崩溃] {str(e)}", file=sys.stderr)
        return []