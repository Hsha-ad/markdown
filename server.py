# server.py
from flask import Flask, send_from_directory
from pan.routes import init_pan_routes

app = Flask(__name__, static_folder='static')

# 初始化网盘路由
init_pan_routes(app)

# 静态文件路由（原功能不变）
@app.route('/')
def serve_index():
    return send_from_directory('static', 'index.html')

@app.route('/<path:path>')
def serve_static(path):
    return send_from_directory('static', path)

if __name__ == '__main__':
    app.run(port=5000)