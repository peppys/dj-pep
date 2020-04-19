import os
from typing import Dict

from aiohttp import ClientSession


async def find_song(query: str) -> Dict:
    session = ClientSession()
    response = await session.get(
        url='https://amp-api.music.apple.com/v1/catalog/us/search',
        headers={'Authorization': f'Bearer {os.getenv("ITUNES_API_TOKEN")}'},
        params={
            'term': query,
            'types': 'artists%2Csongs',
            'limit': 10,
        })
    response.raise_for_status()
    response_json = await response.json()

    songs = response_json['results']['songs']['data']
    songs = [song for song in songs if len(song['attributes']['previews']) > 0]

    if len(songs) == 0:
        raise Exception('Sorry could not find track')

    song = songs[0]

    return {
        'name': song['attributes']['name'],
        'artists': [{'name': song['attributes']['artistName']}],
        'album_name': song['attributes']['albumName'],
        'preview_url': song['attributes']['previews'][0]['url'],
        'image_url': song['attributes']['artwork']['url'].replace('{w}', '750').replace('{h}',
                                                                                        '750'),
        'source': 'itunes',
    }
