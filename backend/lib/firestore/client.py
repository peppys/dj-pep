import os
from enum import Enum
from typing import Dict, List

import firebase_admin
from firebase_admin import credentials
from firebase_admin import firestore
from google.cloud.firestore_v1 import DocumentReference

cred = credentials.ApplicationDefault()
firebase_admin.initialize_app(cred, {
    'projectId': os.getenv('GOOGLE_PROJECT_ID'),
})

db = firestore.client()


class SongStatus(Enum):
    QUEUED = 'QUEUED'
    PLAYING = 'PLAYING'
    PLAYED = 'PLAYED'


def add_song(data: Dict) -> DocumentReference:
    """
    Adds song data to queue
    :param data:
    :return:
    """
    doc_ref = db.collection('songs').document()
    doc_ref.set(data)

    return doc_ref


def find_songs_by_status(status: SongStatus) -> List[Dict]:
    docs = db.collection('songs').where('status', '==', status.value).stream()

    return [{**{'id': doc.id}, **doc.to_dict()} for doc in docs]


def update_by_id(song_id: str, updates: Dict):
    doc_ref: DocumentReference = db.collection('songs').document(song_id)
    doc_ref.update(updates)
