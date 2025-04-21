from flask import Flask
from pan.routes import init_pan_routes
import asyncio
from flask_async import FlaskAsync

app = Flask(__name__)
async_app = FlaskAsync(app)

init_pan_routes(app)

if __name__ == '__main__':
    asyncio.run(async_app.run_async(host='0.0.0.0', port=5000))