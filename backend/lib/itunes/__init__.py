import os
from typing import Dict

from aiofiles import tempfile
from aiohttp import ClientSession
from mutagen.mp4 import MP4


async def find_song(query: str) -> Dict:
    session = ClientSession()
    response = await session.get(
        url='https://amp-api.music.apple.com/v1/catalog/us/search',
        headers={'Authorization': f'Bearer {os.getenv("ITUNES_API_TOKEN")}', 'Origin': 'https://music.apple.com'},
        params={
            'term': query,
            'types': 'artists,songs',
            'limit': 10,
        })
    response.raise_for_status()
    response_json = await response.json()

    songs = response_json['results']['songs']['data']
    songs = [song for song in songs if len(song['attributes']['previews']) > 0]

    if len(songs) == 0:
        raise Exception('Sorry could not find track')

    song = songs[0]
    preview_url = song['attributes']['previews'][0]['url']
    async with tempfile.NamedTemporaryFile() as fp:
        response = await session.get(preview_url)
        await fp.write(await response.read())
        audio = MP4(fp.name)

    return {
        'name': song['attributes']['name'],
        'artists': [{'name': song['attributes']['artistName']}],
        'album_name': song['attributes']['albumName'],
        'preview_url': preview_url,
        'preview_length': min(30, int(audio.info.length)), # cap at 30 seconds
        'image_url': song['attributes']['artwork']['url'].replace('{w}', '750').replace('{h}',
                                                                                        '750'),
        'source': 'itunes',
    }
