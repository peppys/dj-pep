import json

from google.cloud import tasks_v2

client = tasks_v2.CloudTasksClient()

print(client)

parent = client.queue_path(project='personal-site-staging-a449f',
                           location='us-central1',
                           queue='dj-pep-song-player')

url = 'https://c6f41c3d.ngrok.io/task-handlers/song-player'
payload = {'song_id': 1}

task = {'http_request': {'http_method': 'POST',
                         'url': 'https://f43f7bd2.ngrok.io/task-handlers/song-player',
                         'body': json.dumps(payload).encode()}}

response = client.create_task(parent, task)

print(f'Created task {response.name}')

print(response)
