import logging
from datetime import datetime, timezone
import traceback

from sanic import Blueprint
from sanic.request import Request
from sanic.response import text

from lib.firestore.client import add_to_song_queue
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

        song.update({
            'status': 'QUEUED',
            'added_by': from_phone_number,
            'added_at': datetime.now(timezone.utc).isoformat(),
        })

        add_to_song_queue(song)
    except Exception as e:
        logging.error(
            f'Could not search spotify for track: {str(e)} {traceback.format_exc()}')

        return text('Sorry I had trouble with that. Please try a different song!', 200)

    return text('Gotchu fam 🙏🏾. Your song will play shortly...', 200)
