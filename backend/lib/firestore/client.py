import os
from enum import Enum
from typing import Dict, List, Optional

import firebase_admin
from firebase_admin import credentials
from firebase_admin import firestore
from google.cloud.firestore_v1 import DocumentReference, DocumentSnapshot

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


def add_contact(phone_number: str, name: str) -> DocumentReference:
    doc_ref = db.collection('phone_book').document(phone_number)
    doc_ref.set({'name': name})

    return doc_ref


def find_contact(phone_number: str) -> Optional[DocumentReference]:
    try:
        doc_ref = db.collection('phone_book').document(phone_number).get()
        if not doc_ref.exists:
            return None

        return doc_ref
    except Exception:
        return None


def find_songs_by_status_and_preview_url(status: SongStatus, preview_url: str) -> List[Dict]:
    docs = db.collection('songs').where('status', '==', status.value).where('preview_url', '==',
                                                                            preview_url).stream()

    return [{**{'id': doc.id}, **doc.to_dict()} for doc in docs]


def find_songs_by_status(status: SongStatus) -> List[Dict]:
    docs = db.collection('songs').where('status', '==', status.value).stream()

    return [{**{'id': doc.id}, **doc.to_dict()} for doc in docs]


def find_song_by_id(song_id: str) -> Optional[Dict]:
    doc: DocumentSnapshot = db.collection('songs').document(song_id).get()
    if not doc.exists:
        return None

    return {**{'id': doc.id}, **doc.to_dict()}


def update_by_id(song_id: str, updates: Dict):
    doc_ref: DocumentReference = db.collection('songs').document(song_id)
    doc_ref.update(updates)
