import requests
from bs4 import BeautifulSoup
import re
import sys
from urllib.parse import quote
from core.utils import check_valid

def search_ysxjjkl(keyword):
    """原封不动迁移您的爬虫代码"""
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
        
        # 以下是您原有的解析逻辑，完全不变
        for item in soup.select('.resource-item, .search-result'):
            try:
                # 优先获取data-title属性，其次获取标题元素文本
                title = item.get('data-title') or item.select_one('.title, h3').get_text(strip=True)
                # 清理标题中的多余空格和特殊字符
                title = re.sub(r'\s+', ' ', title).strip()
                
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
                    'title': title[:100],  # 保留完整文件名
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
                # 从链接文本中提取更详细的文件名
                link_text = a.get_text(strip=True)
                title = link_text if link_text and len(link_text) > 5 else "百度网盘资源"
                
                results.append({
                    'title': title,  # 使用实际文件名
                    'url': a['href'],
                    'source': 'ysxjjkl',
                    'valid': 'pwd=' in a['href']
                })
        
        print(f"[有效结果] 找到 {len(results)} 条资源", file=sys.stderr)
        return results

    except Exception as e:
        print(f"[爬虫崩溃] {str(e)}", file=sys.stderr)
        return []