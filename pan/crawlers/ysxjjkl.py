def search_ysxjjkl(keyword):
    """修复版爬虫，确保能返回所有相关资源"""
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
        
        # 解析所有资源项
        for item in soup.select('.resource-item, .search-result, .related-item'):
            try:
                # 提取完整标题（保留原标题不做修改）
                title = item.select_one('.title, h3, .file-name').get_text(strip=True)
                
                # 移除关键词过滤条件（这是导致找不到资源的原因）
                # if not re.search(r'狂飙|风暴|短剧|打工人', title, re.IGNORECASE):
                #     continue
                
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
                
                # 判断是否为精准匹配
                is_main = keyword.lower() in title.lower()
                
                # 构建结果对象
                result = {
                    'title': title,
                    'url': link['href'],
                    'source': '影视集结号',
                    'password': pwd or '1234',
                    'valid': bool(pwd),
                    'type': 'main' if is_main else 'related'
                }
                
                results.append(result)
                
            except Exception as e:
                print(f"[解析异常] {str(e)}", file=sys.stderr)
                continue
        
        # 按相关性排序：精准匹配在前，相关资源在后
        results.sort(key=lambda x: (x['type'] == 'main', x['title']))
        
        return results if results else []

    except Exception as e:
        print(f"[爬虫崩溃] {str(e)}", file=sys.stderr)
        return []
