import logging
from datetime import datetime, timezone
import traceback

from sanic import Blueprint
from sanic.request import Request
from sanic.response import text

from lib.cloudtasks.client import create_task_to_play_song
from lib.firestore.client import add_song, find_contact, SongStatus, \
    find_songs_by_status_and_preview_url
from lib.spotify.client import find_song

webhooks_router = Blueprint('webhooks_bp', url_prefix='/webhooks')


@webhooks_router.post('/twilio')
async def twilio_handler(request: Request):
    """
    :param request:
    :return:
    """
    logging.info(request)

    request_data = request.form

    logging.info(f'Received request: {request_data}')

    try:
        song_search_query = request_data['Body'][0]
        from_phone_number = request_data['From'][0]

        logging.info(f'Found track_search_query: {song_search_query} from {from_phone_number}')

        song = find_song(song_search_query)

        logging.info(f'Found song {song}')

        if song['preview_url'] is None:
            raise Exception('No preview url found')

        same_songs_queued = find_songs_by_status_and_preview_url(status=SongStatus.QUEUED,
                                                                 preview_url=song['preview_url'])
        if len(same_songs_queued) > 0:
            raise Exception('Song is already queued')

        song.update({
            'status': SongStatus.QUEUED.value,
            'added_by': from_phone_number,
            'added_at': datetime.now(timezone.utc).isoformat(),
        })

        contact = find_contact(from_phone_number)
        if contact:
            song.update({'added_by_name': contact.get('name')})

        song_doc = add_song(song)

        create_task_to_play_song(song_id=song_doc.id, song_url=song['preview_url'])
    except Exception as e:
        logging.error(
            f'Could not search spotify for track: {str(e)} {traceback.format_exc()}')

        return text('Sorry I had trouble with that. Please try a different song!', 200)

    return text('Gotchu fam 🙏🏾. Your song will play shortly...', 200)
