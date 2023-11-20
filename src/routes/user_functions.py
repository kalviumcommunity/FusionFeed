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


def create_post():
    
    blog_posts = []  # A list to store blog posts

    try:
        data = request.get_json()
        email = request.headers.get('email')
        password = request.headers.get('password')

        if not (email and password):
            return jsonify({'error': 'Missing email or password headers'}), 400

        doc_data = AuthValidation.Validate(email, password)

        if not doc_data:
            return jsonify({'error': 'Invalid email or password'}), 401

        title = data.get('title')
        content = data.get('content')
        author = doc_data

        if not (title and content):
            return jsonify({'error': 'Missing title or content'}), 400

        post_handler = BlogPostHandler()
        post_data = post_handler.create_data(title, content, author)

        blog_posts.append(post_data)

        return jsonify({'message': 'Blog post created', 'post': post_data}), 201

    except Exception as e:
        return jsonify({'error': str(e)}), 500
