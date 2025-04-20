import re
import time
from memory_profiler import profile
from bs4 import BeautifulSoup

class StableCrawler:
    def __init__(self):
        self.request_interval = 2  # 请求间隔(秒)
        self.max_retries = 3
        self.timeout = 10

    @profile
    def safe_search(self, keyword):
        """内存安全的搜索方法"""
        try:
            for attempt in range(self.max_retries):
                try:
                    results = self._search_with_retry(keyword)
                    return self._trim_memory(results)  # 内存优化
                except Exception as e:
                    if attempt == self.max_retries - 1:
                        raise
                    time.sleep(self.request_interval)
        except Exception as e:
            return {'error': str(e), 'code': 500}

    def _search_with_retry(self, keyword):
        # 实现带重试的逻辑
        pass

    def _trim_memory(self, data):
        """优化内存占用"""
        if isinstance(data, list):
            return [item for item in data if item.get('valid')]
        return data