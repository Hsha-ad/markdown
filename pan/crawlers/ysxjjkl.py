import requests
from bs4 import BeautifulSoup
import re
from urllib.parse import quote

def search_ysxjjkl(keyword):
    url = f"https://ysxjjkl.souyisou.top/?search={quote(keyword)}"
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
    }
    
    try:
        response = requests.get(url, headers=headers)
        soup = BeautifulSoup(response.text, 'html.parser')
        results = []
        
        # 修改解析逻辑，提取具体资源名称
        for item in soup.select('.resource-item'):
            try:
                # 优先获取标题元素
                title_elem = item.select_one('.title, h3, .name')
                title = title_elem.get_text(strip=True) if title_elem else "未命名资源"
                
                # 获取网盘链接
                link = item.find('a', href=True)
                if not link:
                    continue
                    
                # 获取密码（如果有）
                pwd = None
                pwd_elem = item.select_one('.pwd-btn, .copy-pwd, .password')
                if pwd_elem and 'data-pwd' in pwd_elem.attrs:
                    pwd = pwd_elem['data-pwd']
                elif pwd_elem:
                    match = re.search(r'[a-zA-Z0-9]{4}', pwd_elem.get_text())
                    pwd = match.group() if match else None
                
                # 构建结果对象
                result = {
                    'title': title,  # 这里返回实际资源名称
                    'url': link['href'],
                    'source': '影视集结号',
                    'valid': bool(pwd)
                }
                
                # 添加密码到URL（如果需要）
                if pwd and 'pwd=' not in result['url']:
                    result['url'] += f"?pwd={pwd}" if '?' not in result['url'] else f"&pwd={pwd}"
                
                results.append(result)
                
            except Exception as e:
                print(f"解析条目时出错: {e}")
                continue
        
        return results
        
    except Exception as e:
        print(f"爬取过程中出错: {e}")
        return []
