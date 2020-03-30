import logging
import os

from api.app import app

if __name__ == '__main__':
    logging.getLogger().setLevel(logging.DEBUG)
    app.run(host='0.0.0.0', port=os.getenv('API_PORT', 8000))
