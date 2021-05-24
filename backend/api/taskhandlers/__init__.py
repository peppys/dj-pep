import logging
from asyncio import sleep
from datetime import datetime
from json import loads

from sanic import Blueprint
from sanic.request import Request
from sanic.response import json

from lib.firestore.client import find_song_by_id, find_songs_by_status, SongStatus, update_by_id

task_handlers_router = Blueprint('task_handlers_bp', url_prefix='/task-handlers')


@task_handlers_router.post('/song-player')
async def song_player_handler(request: Request):
    logging.info(f'Received request: {request.body}')
    payload = loads(request.body.decode())
    logging.info(f'Parsed payload: {payload}')

    song = find_song_by_id(payload['song_id'])
    if song is None:
        logging.error(f'Could not find song with id {payload["song_id"]}')
        return json({'ok': True}, status=200)

    if song['status'] != SongStatus.QUEUED.value:
        logging.error(f'Unexpected status {song["status"]} for song {payload["song_id"]}')
        return json({'ok': True}, status=200)

    # update any songs that are playing, in-case the last task errored out
    playing_songs = find_songs_by_status(SongStatus.PLAYING)
    for playing_song in playing_songs:
        update_by_id(playing_song['id'], {'status': SongStatus.PLAYED.value})

    update_by_id(song['id'], {'status': SongStatus.PLAYING.value,
                              'started_playing_at': datetime.utcnow().isoformat()})

    length = song['preview_length'] or 30
    print(f'Waiting {length} seconds')

    await sleep(length)

    update_by_id(song['id'], {'status': SongStatus.PLAYED.value,
                              'finished_playing_at': datetime.utcnow().isoformat()})

    return json({'ok': True}, status=200)
