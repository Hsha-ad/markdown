import re
import jieba
from bs4 import BeautifulSoup
from urllib.parse import quote
from difflib import SequenceMatcher

class YSXJJKLCrawler:
    def __init__(self):
        self.base_url = "https://www.ysxjjkl.com/search?q={}"
        jieba.add_word('[短剧]')
        jieba.add_word('提取码')

    def search(self, keyword):
        search_url = self.base_url.format(quote(keyword))
        try:
            html = self._fetch_html(search_url)
            return self.parse_results(html, keyword)
        except Exception as e:
            print(f"爬取失败: {str(e)}")
            return []

    def _fetch_html(self, url):
        # 实现HTTP请求（需根据实际需求补充）
        pass

    def parse_results(self, html, keyword):
        soup = BeautifulSoup(html, 'lxml')
        results = []
        
        for item in soup.select('.resource-item'):
            title_tag = item.select_one('.title')
            if not title_tag:
                continue
                
            raw_title = title_tag.get_text(strip=True)
            processed_title = self._process_title(keyword, raw_title)
            
            link_tag = item.select_one('.link[href*="pan.baidu.com"]')
            pwd_tag = item.select_one('.pwd')
            
            if link_tag and pwd_tag:
                results.append({
                    'title': processed_title,
                    'original_title': raw_title,
                    'link': link_tag['href'],
                    'pwd': pwd_tag.get_text(strip=True).replace('提取码：', ''),
                    'is_short': self._is_short_play(raw_title),
                    'relevance': self._calculate_relevance(keyword, raw_title)
                })
        
        # 按相关性排序
        return sorted(results, key=lambda x: x['relevance'], reverse=True)

    def _process_title(self, keyword, title):
        """保留原标题结构的关键词处理"""
        # 短剧特殊处理
        if self._is_short_play(title):
            return title
        
        # 精确匹配处理
        if keyword in title:
            return title
            
        # 相似内容处理
        if SequenceMatcher(None, keyword, title).ratio() > 0.6:
            return f"{keyword}相关：{title}"
            
        return title

    def _is_short_play(self, title):
        """短剧识别"""
        return '[短剧]' in title or '短剧' in title or '集全' in title

    def _calculate_relevance(self, keyword, title):
        """基于编辑距离和词频的相关性计算"""
        keyword_chars = set(keyword)
        title_chars = set(title)
        
        # 字符重合度
        char_overlap = len(keyword_chars & title_chars) / len(keyword_chars)
        
        # 词频权重
        word_weights = {
            '完整版': 1.5,
            '高清': 1.2,
            '全集': 1.3,
            '[短剧]': 0.8
        }
        
        weight = sum(word_weights.get(word, 1) for word in jieba.cut(title))
        
        return char_overlap * weight

    def _fetch_html(self, url):
        # 实现实际的HTTP请求
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
        }
        response = requests.get(url, headers=headers, timeout=10)
        response.raise_for_status()
        return response.text