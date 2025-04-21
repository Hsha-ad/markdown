# pan/routes.py
from flask import request, jsonify
from .services import search_pan_resources

def init_pan_routes(app):
    """原封不动迁移您的API路由逻辑"""
    pass