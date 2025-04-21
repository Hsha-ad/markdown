# pan/services.py
import nltk
import spacy
import jieba
from .crawlers.ysxjjkl import search_ysxjjkl

# 下载 NLTK 必要的数据
nltk.download('punkt')
# 加载 SpaCy 英文模型
nlp_en = spacy.load('en_core_web_sm')
# 确保中文分词
jieba.initialize()

def process_natural_language_query(query):
    # 判断是否为中文
    if any('\u4e00' <= char <= '\u9fff' for char in query):
        # 中文分词
        tokens = jieba.lcut(query)
    else:
        # 英文分词和处理
        doc = nlp_en(query)
        tokens = [token.text for token in doc]
    # 简单示例：提取关键词，可根据需求扩展
    keywords = [token for token in tokens if token.isalnum()]
    return ' '.join(keywords)

def search_pan_resources(keyword):
    """统一调用所有网盘爬虫（目前只有影视集结号）"""
    # 处理自然语言查询
    processed_keyword = process_natural_language_query(keyword)
    return {
        'ysxjjkl': search_ysxjjkl(processed_keyword)  # 保持原功能不变
    }