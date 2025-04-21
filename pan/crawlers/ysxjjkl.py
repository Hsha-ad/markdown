import requests
from bs4 import BeautifulSoup
import re
import sys
from urllib.parse import quote
from core.utils import check_valid
import logging

# 配置日志
logging.basicConfig(level=logging.ERROR)
logger = logging.getLogger(__name__)

def search_ysxjjkl(keyword):
    try:
        url = f"https://ysxjjkl.souyisou.top/?search={quote(keyword)}"
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36',
            'Referer': 'https://ysxjjkl.souyisou.top/',
            'X-Requested-With': 'XMLHttpRequest'
        }

        logger.info(f"[新版爬虫] 请求URL: {url}")
        response = requests.get(url, headers=headers, timeout=15)
        response.raise_for_status()

        soup = BeautifulSoup(response.text, 'html.parser')
        results = []

        for item in soup.select('.box'):
            try:
                info_div = item.find('div', class_='info')
                if info_div:
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
                logger.error(f"[解析异常] {str(e)}", exc_info=True)
                continue

        if not results:
            logger.warning("[警告] 主解析方案无结果，尝试备用方案")
            for a in soup.find_all('a', href=re.compile(r'pan\.baidu\.com/s/[^\s]+')):
                results.append({
                    'title': a.get_text(strip=True) or "百度网盘资源",
                    'url': a['href'],
                    'source': 'ysxjjkl',
                    'valid': 'pwd=' in a['href']
                })

        logger.info(f"[有效结果] 找到 {len(results)} 条资源")
        return results

    except requests.RequestException as e:
        logger.error(f"[爬虫请求出错] {str(e)}", exc_info=True)
        return []
    except Exception as e:
        logger.error(f"[爬虫崩溃] {str(e)}", exc_info=True)
        return []