import requests
from bs4 import BeautifulSoup
import re
import sys
from urllib.parse import quote

def search_ysxjjkl(keyword):
    """改进版爬虫，支持返回相关衍生资源"""
    try:
        url = f"https://ysxjjkl.souyisou.top/?search={quote(keyword)}"
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36',
            'Referer': 'https://ysxjjkl.souyisou.top/',
            'X-Requested-With': 'XMLHttpRequest'
        }
        
        response = requests.get(url, headers=headers, timeout=15)
        response.raise_for_status()
        
        soup = BeautifulSoup(response.text, 'html.parser')
        results = []
        
        # 解析所有资源项，包括主资源和相关资源
        for item in soup.select('.resource-item, .search-result, .related-item'):
            try:
                # 提取完整标题（保留原标题不做修改）
                title = item.select_one('.title, h3, .file-name').get_text(strip=True)
                
                # 跳过不包含关键词的完全不相关结果
                if not re.search(r'狂飙|风暴|短剧|打工人', title, re.IGNORECASE):
                    continue
                
                # 提取网盘链接
                link = item.find('a', href=lambda x: x and ('pan.baidu.com' in x or 'aliyundrive.com' in x))
                if not link:
                    continue
                
                # 提取密码
                pwd = None
                pwd_btn = item.select_one('.pwd-btn, .copy-pwd')
                if pwd_btn and pwd_btn.get('data-pwd'):
                    pwd = pwd_btn['data-pwd']
                else:
                    pwd_text = item.select_one('.password:not(:empty)')
                    if pwd_text:
                        pwd_match = re.search(r'[a-zA-Z0-9]{4}', pwd_text.get_text())
                        pwd = pwd_match.group() if pwd_match else None
                
                # 构建结果对象
                result = {
                    'title': title,  # 保留原标题不做修改
                    'url': link['href'],
                    'source': '影视集结号',
                    'password': pwd or '1234',
                    'valid': bool(pwd),
                    'type': 'related' if 'related' in item.get('class', []) else 'main'
                }
                
                results.append(result)
                
            except Exception as e:
                print(f"[解析异常] {str(e)}", file=sys.stderr)
                continue
        
        # 按相关性排序：完全匹配的在前，相关资源在后
        results.sort(key=lambda x: (x['type'] == 'main', x['title']))
        
        return results

    except Exception as e:
        print(f"[爬虫崩溃] {str(e)}", file=sys.stderr)
        return []
