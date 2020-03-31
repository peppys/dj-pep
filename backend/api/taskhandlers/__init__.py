import logging
from asyncio import sleep
from datetime import datetime
from json import loads

import requests

from mutagen.mp3 import MP3
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

    playing_songs = find_songs_by_status(SongStatus.PLAYING)
    if len(playing_songs) > 0:
        logging.error(f'Found a song still playing {playing_songs}. Payload: {payload}')

        return json({'error': 'A song is still playing!'}, status=400)

    response = requests.get(payload['song_url'])
    response.raise_for_status()

    with open('./song.mp3', mode='wb') as f:
        f.write(response.content)

    update_by_id(payload['song_id'], {'status': SongStatus.PLAYING.value,
                                      'started_playing_at': datetime.utcnow().isoformat()})

    audio = MP3('./song.mp3')

    print(f'Waiting {audio.info.length} seconds')

    await sleep(audio.info.length)

    update_by_id(payload['song_id'], {'status': SongStatus.PLAYED.value,
                                      'finished_playing_at': datetime.utcnow().isoformat()})

    return json({'ok': True}, status=200)
