import logging
from json import loads

from sanic import Blueprint
from sanic.request import Request
from sanic.response import json

task_handlers_router = Blueprint('task_handlers_bp', url_prefix='/task-handlers')


@task_handlers_router.post('/song-player')
async def song_player_handler(request: Request):
    logging.info(f'Received request: {request.body}')

    payload = loads(request.body.decode())

    logging.info(f'Parsed payload: {payload}')

    return json({'ok': True}, status=200)
