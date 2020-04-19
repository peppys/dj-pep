import logging
import os
from typing import Dict

from spotipy import Spotify
from spotipy.oauth2 import SpotifyClientCredentials

client = Spotify(
    client_credentials_manager=SpotifyClientCredentials(client_id=os.getenv('SPOTIFY_CLIENT_ID'),
                                                        client_secret=os.getenv(
                                                            'SPOTIFY_CLIENT_SECRET')))


def find_song(query: str) -> Dict:
    """
    Searches for a song via spotify API
    :param query:
    :return:
    """
    results = client.search(q=query, type='track', limit=20)

    songs = list(filter(lambda x: x['preview_url'], results['tracks']['items']))

    if len(songs) == 0:
        raise Exception('Sorry could not find track')

    song = songs[0]

    logging.info(f'Found full song {song}')

    return {
        'name': song['name'],
        'artists': list(map(lambda x: {
            'name': x['name'],
        }, song['artists'])),
        'album_name': song['album']['name'],
        'preview_url': song['preview_url'],
        'image_url': song['album']['images'][0]['url'],
        'source': 'spotify'
    }
