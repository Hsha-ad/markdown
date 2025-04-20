from flask import Flask, jsonify, request

app = Flask(__name__)

# 定义 Vercel 直接访问的接口路径（如根路径 /api/search）
@app.route('/api/search', methods=['GET'])
def search():
    keyword = request.args.get('keyword')
    if not keyword:
        return jsonify({'error': '关键词不能为空'}), 400
    # 这里调用你的爬虫逻辑获取 results
    results = []  # 替换为实际数据
    return jsonify({'results': results})

if __name__ == '__main__':
    app.run(port=3000)  # Vercel 环境变量会覆盖端口，此处可设为任意
