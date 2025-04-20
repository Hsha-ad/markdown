import json
from datetime import datetime
from crawlers.ysxjjkl import YSXJJKLCrawler

class SearchService:
    def __init__(self):
        self.crawler = YSXJJKLCrawler()
        self.cache = {}

    def search_resources(self, keyword):
        cache_key = f"{keyword.lower()}_{datetime.now().strftime('%Y%m%d')}"
        
        if cache_key in self.cache:
            return self.cache[cache_key]
            
        results = self.crawler.search(keyword)
        processed = self._process_results(keyword, results)
        
        self.cache[cache_key] = processed
        return processed

    def _process_results(self, keyword, raw_results):
        """结果分类处理"""
        categorized = {
            'exact_matches': [],
            'related_content': [],
            'short_plays': []
        }
        
        for item in raw_results:
            if item['is_short']:
                categorized['short_plays'].append(item)
            elif keyword in item['original_title']:
                categorized['exact_matches'].append(item)
            else:
                categorized['related_content'].append(item)
                
        return categorized

    def get_formatted_results(self, keyword):
        """前端展示专用格式"""
        raw_data = self.search_resources(keyword)
        formatted = []
        
        # 精确匹配
        if raw_data['exact_matches']:
            formatted.append({'type': 'title', 'text': f"🔍 精确匹配：{keyword}"})
            formatted.extend(self._format_items(raw_data['exact_matches']))
        
        # 相关资源
        if raw_data['related_content']:
            formatted.append({'type': 'title', 'text': "📚 相关资源"})
            formatted.extend(self._format_items(raw_data['related_content']))
        
        # 短剧资源
        if raw_data['short_plays']:
            formatted.append({'type': 'title', 'text': "🎬 短剧资源"})
            formatted.extend(self._format_items(raw_data['short_plays']))
            
        return formatted

    def _format_items(self, items):
        return [{
            'type': 'resource',
            'title': item['title'],
            'link': item['link'],
            'pwd': item['pwd'],
            'is_short': item['is_short']
        } for item in items]