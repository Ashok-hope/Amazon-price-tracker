

import firebase_admin
from firebase_admin import credentials, firestore, auth
import os
from typing import Dict, Any
from dotenv import load_dotenv


# Load environment variables from .env
load_dotenv()

# Get credentials path from environment variable
cred_path = os.getenv("FIREBASE_CREDENTIALS", "serviceAccountKey.json")

# Initialize Firebase Admin SDK
try:
    cred = credentials.Certificate(cred_path)
    firebase_admin.initialize_app(cred)
except ValueError:
    # App already initialized
    pass

# Firestore client
db = firestore.client()

class FirebaseService:
    @staticmethod
    def get_collection(collection_name: str):
        return db.collection(collection_name)
    
    @staticmethod
    def add_document(collection_name: str, data: Dict[Any, Any]) -> str:
        doc_ref = db.collection(collection_name).add(data)
        return doc_ref[1].id
    
    @staticmethod
    def get_document(collection_name: str, doc_id: str):
        doc = db.collection(collection_name).document(doc_id).get()
        if doc.exists:
            data = doc.to_dict() or {}
            return {"id": doc.id, **data}
        return None
    
    @staticmethod
    def update_document(collection_name: str, doc_id: str, data: Dict[Any, Any]):
        db.collection(collection_name).document(doc_id).update(data)
    
    @staticmethod
    def delete_document(collection_name: str, doc_id: str):
        db.collection(collection_name).document(doc_id).delete()
    
    @staticmethod
    def query_documents(collection_name: str, field: str, operator: str, value: Any):
        docs = db.collection(collection_name).where(field, operator, value).stream()
        return [{"id": doc.id, **doc.to_dict()} for doc in docs]

firebase_service = FirebaseService()
