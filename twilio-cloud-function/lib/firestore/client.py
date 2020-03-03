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


def upsert_instagram_profile(username: str, data: Dict):
    """
    Upserts instagram profile data to firestore
    :param username:
    :param data:
    :return:
    """
    doc_ref = db.collection('instagram_profiles').document(username)
    doc_ref.set(data)
