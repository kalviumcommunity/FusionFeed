from flask import jsonify, request
from src.models.doc_model import BlogPostHandler
from src.middlewares.auth_mid import AuthValidation

from pymongo import MongoClient
from bson import ObjectId  # Import ObjectId from bson
import os

MONGO_URI = os.getenv('MONGO')
mongo_client = MongoClient(MONGO_URI)
db = mongo_client.test
posts_collection = db["blog_posts"]

def create_post():
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

        # Insert the post into MongoDB
        result = posts_collection.insert_one(post_data)

        return jsonify({'message': 'Blog post created', 'post_id': str(result.inserted_id)}), 201

    except Exception as e:
        return jsonify({'error': str(e)}), 500

def get_posts():
    try:
        # Retrieve all posts from MongoDB
        posts = list(posts_collection.find())

        # Convert ObjectId to string for JSON serialization
        for post in posts:
            post['_id'] = str(post['_id'])

        return jsonify({'posts': posts}), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

def get_post(id):
    try:
        # Find the post with the given ID in MongoDB
        post = posts_collection.find_one({'_id': ObjectId(id)})

        if post:
            # Convert ObjectId to string for JSON serialization
            post['_id'] = str(post['_id'])
            return jsonify({'post': post}), 200
        else:
            return jsonify({'error': 'Post not found'}), 404
    except Exception as e:
        return jsonify({'error': str(e)}), 500

def update_post(id):
    try:
        data = request.get_json()
        title = data.get('title')
        content = data.get('content')

        # Find the post with the given ID in MongoDB
        post = posts_collection.find_one({'_id': ObjectId(id)})

        if not post:
            return jsonify({'error': 'Post not found'}), 404

        # Update the post with the new data in MongoDB
        posts_collection.update_one({'_id': ObjectId(id)}, {'$set': {'title': title, 'content': content}})

        # Return the updated post
        updated_post = posts_collection.find_one({'_id': ObjectId(id)})

        # Convert ObjectId to string for JSON serialization
        updated_post['_id'] = str(updated_post['_id'])

        return jsonify({'message': 'Blog post updated', 'post': updated_post}), 200

    except Exception as e:
        return jsonify({'error': str(e)}), 500

def delete_post(id):
    try:
        # Delete the post with the given ID from MongoDB
        result = posts_collection.delete_one({'_id': ObjectId(id)})

        if result.deleted_count > 0:
            return jsonify({'message': 'Blog post deleted'}), 200
        else:
            return jsonify({'error': 'Post not found'}), 404

    except Exception as e:
        return jsonify({'error': str(e)}), 500
