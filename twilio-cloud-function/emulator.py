import logging
import os

from flask import Flask, request

from twilio_message_handler import twilio_message_handler

PORT = int(os.getenv('CLOUD_FUNCTIONS_EMULATOR_PORT', '8081'))

app = Flask(__name__)


@app.route('/twilio_message_handler', methods=['DELETE', 'GET', 'PATCH', 'POST', 'PUT'])
def twilio_message_handler_route():
    return twilio_message_handler(request)


if __name__ == '__main__':
    logging.getLogger().setLevel(logging.INFO)
    app.run('0.0.0.0', PORT, debug=True, threaded=True)
