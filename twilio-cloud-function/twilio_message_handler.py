import logging

from flask import Request
from twilio.twiml.messaging_response import MessagingResponse

from lib.firestore.client import upsert_instagram_profile
from lib.instagram.client import fetch_instagram_profile


def twilio_message_handler(request: Request):
    """
    :param request:
    :return:
    """
    logging.info(request)

    request_data = request.form

    logging.info(f'Received request: {request_data}')

    resp = MessagingResponse()

    try:
        username = request_data['body']
        username = username.strip()

        profile_data = fetch_instagram_profile(username)
        upsert_instagram_profile(username, profile_data)
    except Exception as e:
        logging.info(f'Could not parse instagram data for request {request_data}')
        resp.message(f'Sorry I had trouble with that. Please try again!')
        return str(resp), 200

    logging.info(f'Found profile data {profile_data}')
    resp.message(f'Got your request! {profile_data}')

    return str(resp), 200
