import requests
from bs4 import BeautifulSoup
import re
import sys
from urllib.parse import quote

def search_ysxjjkl(keyword):
    """修复版爬虫，确保能返回所有相关资源"""
    try:
        url = f"https://ysxjjkl.souyisou.top/?search={quote(keyword)}"
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36',
            'Referer': 'https://ysxjjkl.souyisou.top/',
            'X-Requested-With': 'XMLHttpRequest'
        }
        
        print(f"[爬虫] 正在请求: {url}", file=sys.stderr)
        response = requests.get(url, headers=headers, timeout=15)
        
        # 检查响应内容是否为HTML（可能是被重定向到登录页）
        if '<!DOCTYPE html>' in response.text[:15]:
            print("[错误] 请求被重定向到HTML页面", file=sys.stderr)
            return []
            
        response.raise_for_status()
        
        soup = BeautifulSoup(response.text, 'html.parser')
        results = []
        
        # 解析所有资源项
        for item in soup.select('.resource-item, .search-result, .related-item'):
            try:
                # 提取完整标题
                title_elem = item.select_one('.title, h3, .file-name, a')
                if not title_elem:
                    continue
                    
                title = title_elem.get_text(strip=True)
                if not title:
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
                        pwd = pwd_match.group() if pwd_match else '1234'
                
                # 构建结果对象
                results.append({
                    'title': title,
                    'url': link['href'],
                    'source': '影视集结号',
                    'password': pwd or '1234',
                    'valid': bool(pwd)
                })
                
            except Exception as e:
                print(f"[解析异常] {str(e)}", file=sys.stderr)
                continue
        
        print(f"[爬虫] 找到 {len(results)} 条资源", file=sys.stderr)
        return results if results else []

    except Exception as e:
        print(f"[爬虫崩溃] {str(e)}", file=sys.stderr)
        return []
