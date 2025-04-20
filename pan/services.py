# pan/services.py 完整改造版
import re
import jieba
import requests
from bs4 import BeautifulSoup
from collections import defaultdict

class SearchService:
    def __init__(self):
        self.base_url = "https://目标站API地址/search?q={}"
        jieba.initialize()  # 初始化分词器

    def search_resources(self, keyword):
        """整合爬虫与分类的核心方法"""
        try:
            # 1. 获取网页数据
            html = self._fetch_html(keyword)
            
            # 2. 解析并分类结果
            raw_results = self._parse_html(html)
            return self._classify_results(raw_results, keyword)
            
        except Exception as e:
            return {"error": str(e)}

    def _fetch_html(self, keyword):
        """封装HTTP请求"""
        url = self.base_url.format(requests.utils.quote(keyword))
        headers = {'User-Agent': 'Mozilla/5.0 (Vercel Serverless)'}
        response = requests.get(url, headers=headers, timeout=10)
        response.raise_for_status()
        return response.text

    def _parse_html(self, html):
        """解析HTML结构（适配目标站）"""
        soup = BeautifulSoup(html, 'html.parser')
        results = []
        
        for item in soup.select('.result-item'):
            title = item.select_one('.title').text.strip()
            link = item.select_one('a[href*="pan.baidu.com"]')['href']
            pwd = self._extract_password(item.text)
            
            results.append({
                'title': title,
                'link': link,
                'pwd': pwd
            })
        return results

    def _extract_password(self, text):
        """提取密码（兼容目标站格式）"""
        match = re.search(r'提取码[:：]?\s*(\w{4})', text)
        return match.group(1) if match else ''

    def _classify_results(self, items, keyword):
        """智能分类逻辑"""
        classified = defaultdict(list)
        
        for item in items:
            title = item['title']
            if self._is_short_play(title):
                classified['short_plays'].append(item)
            elif keyword in title:
                classified['exact_matches'].append(item)
            else:
                classified['related'].append(item)
        return dict(classified)

    def _is_short_play(self, title):
        """短剧识别（完全匹配目标站）"""
        return any(kw in title for kw in ['[短剧]', '短剧', '全', '集'])