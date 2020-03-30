import os
from typing import Dict

import firebase_admin
from firebase_admin import credentials
from firebase_admin import firestore
from google.cloud.firestore_v1 import DocumentReference

cred = credentials.ApplicationDefault()
firebase_admin.initialize_app(cred, {
    'projectId': os.getenv('GOOGLE_PROJECT_ID'),
})

db = firestore.client()


def add_song(data: Dict) -> DocumentReference:
    """
    Adds song data to queue
    :param data:
    :return:
    """
    doc_ref = db.collection('songs').document()
    doc_ref.set(data)

    return doc_ref
