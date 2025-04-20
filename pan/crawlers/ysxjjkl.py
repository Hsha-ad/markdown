def search_ysxjjkl(keyword):
    """改进版爬虫，模拟浏览器请求"""
    try:
        url = f"https://ysxjjkl.souyisou.top/?search={quote(keyword)}"
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
            'Referer': 'https://ysxjjkl.souyisou.top/',
            'Accept': 'text/html,application/xhtml+xml',
            'Accept-Language': 'zh-CN,zh;q=0.9',
            'Cache-Control': 'no-cache',
        }
        
        # 使用会话保持连接
        session = requests.Session()
        session.headers.update(headers)
        
        # 添加重试机制
        retry_strategy = requests.adapters.HTTPAdapter(
            max_retries=3,
            pool_connections=10,
            pool_maxsize=100
        )
        session.mount('https://', retry_strategy)
        
        response = session.get(url, timeout=15)
        response.raise_for_status()
        
        # 验证响应内容
        if '请先登录' in response.text:
            raise Exception('需要登录才能访问')
            
        soup = BeautifulSoup(response.text, 'html.parser')
        results = []
        
        # 解析资源项
        for item in soup.select('.resource-item, .search-result'):
            try:
                title = item.select_one('.title, h3, .file-name').get_text(strip=True)
                link = item.find('a', href=lambda x: x and ('pan.baidu.com' in x or 'aliyundrive.com' in x))
                
                if not link:
                    continue
                    
                # 提取密码
                pwd = '1234'  # 默认密码
                pwd_elem = item.select_one('.password, .pwd-btn')
                if pwd_elem:
                    pwd_match = re.search(r'[a-zA-Z0-9]{4}', pwd_elem.get_text())
                    if pwd_match:
                        pwd = pwd_match.group()
                
                results.append({
                    'title': title,
                    'url': link['href'],
                    'password': pwd,
                    'source': '影视集结号'
                })
                
            except Exception as e:
                print(f"解析错误: {str(e)}")
                continue
                
        return results
        
    except Exception as e:
        print(f"爬虫错误: {str(e)}")
        return []
