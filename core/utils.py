import requests
from urllib.parse import urlparse

def check_valid(url):
    """优化后的校验函数，增加URL格式验证"""
    if not url or not isinstance(url, str):
        return False
        
    try:
        parsed = urlparse(url)
        if not all([parsed.scheme, parsed.netloc]):
            return False
            
        if "?pwd=" not in url:
            return False
            
        # 只允许特定域名的校验
        allowed_domains = ['pan.baidu.com', 'aliyundrive.com']
        if not any(domain in parsed.netloc for domain in allowed_domains):
            return False
            
        # 增加请求超时和重试
        for _ in range(2):
            try:
                r = requests.head(url, timeout=3, allow_redirects=True)
                return r.status_code == 200
            except requests.exceptions.Timeout:
                continue
            except:
                return False
                
        return False
    except:
        return False