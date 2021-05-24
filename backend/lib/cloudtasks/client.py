import json
import os

from google.cloud import tasks_v2

client = tasks_v2.CloudTasksClient()


def create_task_to_play_song(song_id: str):
    payload = {'song_id': song_id}

    parent = client.queue_path(project=os.getenv('GOOGLE_PROJECT_ID'),
                               location='us-central1',
                               queue='dj-pep-song-player')

    task = {'http_request': {'http_method': 'POST',
                             'url': f'{os.getenv("TASK_HANDLER_URL")}/task-handlers/song-player',
                             'body': json.dumps(payload).encode()}}

    client.create_task(parent, task)
