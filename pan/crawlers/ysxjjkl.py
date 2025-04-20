import requests
from bs4 import BeautifulSoup
import re
from urllib.parse import quote
import logging

# 设置日志
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def search_ysxjjkl(keyword):
    url = f"https://ysxjjkl.souyisou.top/?search={quote(keyword)}"
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36',
        'Referer': 'https://ysxjjkl.souyisou.top/'
    }
    
    try:
        logger.info(f"开始爬取: {url}")
        response = requests.get(url, headers=headers, timeout=10)
        response.raise_for_status()
        
        soup = BeautifulSoup(response.text, 'html.parser')
        results = []
        
        # 调试：保存网页内容供检查
        with open('debug_page.html', 'w', encoding='utf-8') as f:
            f.write(soup.prettify())
        
        # 多种选择器尝试匹配资源项
        items = soup.select('.resource-item, .item, .result-item, .list-item')
        if not items:
            items = soup.find_all('div', class_=re.compile(r'item|result|resource'))
        
        logger.info(f"找到 {len(items)} 个潜在资源项")
        
        for item in items:
            try:
                # 尝试多种方式获取标题
                title = None
                for selector in ['.title', 'h3', 'h4', '.name', 'a[title]']:
                    elem = item.select_one(selector)
                    if elem and elem.get_text(strip=True):
                        title = elem.get_text(strip=True)
                        break
                
                if not title:
                    title = "未命名资源"
                
                # 获取链接
                link = None
                for selector in ['a[href*="pan.baidu.com"]', 'a[href*="aliyundrive.com"]', 'a[href]']:
                    elem = item.select_one(selector)
                    if elem and elem.get('href'):
                        link = elem['href']
                        break
                
                if not link:
                    continue
                
                # 获取密码
                pwd = None
                pwd_elem = item.select_one('.pwd-btn, .copy-pwd, .password, .pwd')
                if pwd_elem:
                    if 'data-pwd' in pwd_elem.attrs:
                        pwd = pwd_elem['data-pwd']
                    else:
                        match = re.search(r'[a-zA-Z0-9]{4}', pwd_elem.get_text())
                        pwd = match.group() if match else None
                
                # 构建结果
                result = {
                    'title': title[:200],  # 限制长度防止过长
                    'url': link,
                    'source': '影视集结号',
                    'valid': bool(pwd),
                    'password': pwd
                }
                
                # 处理密码
                if pwd and 'pwd=' not in result['url']:
                    result['url'] += f"?pwd={pwd}" if '?' not in result['url'] else f"&pwd={pwd}"
                
                results.append(result)
                logger.info(f"找到资源: {title}")
                
            except Exception as e:
                logger.error(f"解析资源项时出错: {e}")
                continue
        
        logger.info(f"共找到 {len(results)} 个有效资源")
        return results
        
    except Exception as e:
        logger.error(f"爬取过程中出错: {e}")
        return []