import logging
from flask import Flask
from pan.routes import init_pan_routes
import asyncio
from flask_async import FlaskAsync

# 配置日志
logging.basicConfig(level=logging.ERROR)
logger = logging.getLogger(__name__)

app = Flask(__name__)
async_app = FlaskAsync(app)

init_pan_routes(app)

@app.errorhandler(Exception)
def handle_exception(e):
    logger.error(f"An unexpected error occurred: {str(e)}", exc_info=True)
    return jsonify({"error": "An unexpected error occurred. Please try again later."}), 500

if __name__ == '__main__':
    try:
        asyncio.run(async_app.run_async(host='0.0.0.0', port=5000))
    except Exception as e:
        logger.error(f"Failed to start the server: {str(e)}", exc_info=True)