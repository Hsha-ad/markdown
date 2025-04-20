# core/utils.py
import requests

def check_valid(url):
    """原封不动迁移您的校验函数"""
    if "?pwd=" not in url:
        return False
    try:
        r = requests.head(url, timeout=3)
        return r.status_code == 200
    except:
        return False