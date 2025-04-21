from flask import Flask
from pan.routes import pan_bp

app = Flask(__name__, static_folder='static')
app.register_blueprint(pan_bp)


@app.route('/<path:path>')
def serve_static(path):
    return app.send_static_file(path)


@app.route('/')
def index():
    return app.send_static_file('index.html')


if __name__ == '__main__':
    app.run(debug=True)

    