import os
from typing import Dict

import firebase_admin
from firebase_admin import credentials
from firebase_admin import firestore

cred = credentials.ApplicationDefault()
firebase_admin.initialize_app(cred, {
    'projectId': os.getenv('GOOGLE_PROJECT_ID'),
})

db = firestore.client()


def add_to_song_queue(data: Dict):
    """
    Adds song data to queue
    :param data:
    :return:
    """
    doc_ref = db.collection('song_queue').document()
    doc_ref.set(data)
