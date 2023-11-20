from flask import request, Response, jsonify
from src.models.doc_model import DocumentHandler
from src.middlewares.auth_mid import AuthValidation
from src.models.doc_model import DocumentHandler, BlogPostHandler

from pymongo import MongoClient
import os

MONGO = os.getenv('MONGO')
Auth = MongoClient(MONGO).test["OOPs"]

def create_document():
    try:
        data = request.get_json()
        name = data.get('name')
        email = data.get('email')
        password = data.get('password')

        if not (name and email and password):
            return jsonify({'error': 'Missing data'}), 400

        doc_handler = DocumentHandler()
        doc_data = doc_handler.create_data(name, email, password)

        result = Auth.insert_one(doc_data)
        return jsonify({'message': 'Document created', 'document_id': str(result.inserted_id)}), 201

    except Exception as e:
        return jsonify({'error': str(e)}), 500

