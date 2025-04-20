# pan/crawlers/ysxjjkl.py
import requests
from bs4 import BeautifulSoup
import re
import sys
from urllib.parse import quote
from core.utils import check_valid

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
        
        for item in soup.select('.resource-item, .search-result'):
            try:
                # 尝试多种方式提取标题
                title = None
                # 优先使用 data-title 属性
                title = item.get('data-title') 
                if not title:
                    # 尝试从 .title 或 h3 标签中提取
                    title_element = item.select_one('.title, h3')
                    if title_element:
                        title = title_element.get_text(strip=True)
                if not title:
                    # 如果还没有找到，尝试从链接的父元素中提取文本
                    link = item.find('a', href=lambda x: x and ('pan.baidu.com' in x or 'aliyundrive.com' in x))
                    if link:
                        title = link.parent.get_text(strip=True)
                
                if not title:
                    title = "未命名资源"
                
                link = item.find('a', href=lambda x: x and ('pan.baidu.com' in x or 'aliyundrive.com' in x))
                if not link:
                    continue
                
                pwd = None
                pwd_btn = item.select_one('.pwd-btn, .copy-pwd')
                if pwd_btn and pwd_btn.get('data-pwd'):
                    pwd = pwd_btn['data-pwd']
                else:
                    pwd_text = item.select_one('.password:not(:empty)')
                    if pwd_text:
                        pwd = re.search(r'[a-zA-Z0-9]{4}', pwd_text.get_text()).group()
                
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
                results.append({
                    'title': a.get_text(strip=True) or "百度网盘资源",
                    'url': a['href'],
                    'source': 'ysxjjkl',
                    'valid': 'pwd=' in a['href']
                })
        
        print(f"[有效结果] 找到 {len(results)} 条资源", file=sys.stderr)
        return results

    except Exception as e:
        print(f"[爬虫崩溃] {str(e)}", file=sys.stderr)
        return []