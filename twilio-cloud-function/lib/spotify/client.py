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
    results = client.search(q=query, type='track', limit=1)

    if len(results['tracks']['items']) == 0:
        raise Exception('Sorry could not find track')

    song = results['tracks']['items'][0]

    return {
        'name': song['name'],
        'album_name': song['album']['name'],
        'preview_url': song['preview_url'],
        'image_url': song['album']['images'][0]['url']
    }
