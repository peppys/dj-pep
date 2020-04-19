import logging
from asyncio import sleep
from datetime import datetime
from json import loads

import requests

from sanic import Blueprint
from sanic.request import Request
from sanic.response import json

from lib.firestore.client import find_songs_by_status, SongStatus, update_by_id

task_handlers_router = Blueprint('task_handlers_bp', url_prefix='/task-handlers')


@task_handlers_router.post('/song-player')
async def song_player_handler(request: Request):
    logging.info(f'Received request: {request.body}')

    payload = loads(request.body.decode())

    logging.info(f'Parsed payload: {payload}')

    # update any songs that are playing, in-case the last task errored out
    playing_songs = find_songs_by_status(SongStatus.PLAYING)
    for playing_song in playing_songs:
        update_by_id(playing_song['id'], {'status': SongStatus.PLAYED.value})

    response = requests.get(payload['song_url'])
    response.raise_for_status()

    update_by_id(payload['song_id'], {'status': SongStatus.PLAYING.value,
                                      'started_playing_at': datetime.utcnow().isoformat()})

    print(f'Waiting 29 seconds')

    await sleep(29)

    update_by_id(payload['song_id'], {'status': SongStatus.PLAYED.value,
                                      'finished_playing_at': datetime.utcnow().isoformat()})

    return json({'ok': True}, status=200)
