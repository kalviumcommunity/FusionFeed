from flask import Flask, request, jsonify
from auth import AuthValidation
from pymongo import MongoClient
import os
from abc import ABC, abstractmethod

MONGO = os.getenv('MONGO')
Auth = MongoClient(MONGO).test["OOPs"]

app = Flask(__name__)
blog_posts = []  # A list to store blog posts


class DataHandler(ABC):
    @abstractmethod
    def create_data(self, **data):
        pass


class DocumentHandler(DataHandler):
    def create_data(self, name, email, password):
        doc_data = {"name": name, "email": email, "password": password}
        return doc_data


class BlogPostHandler(DataHandler):
    def create_data(self, title, content, author):
        post_data = {"title": title, "content": content, "author": author}
        return post_data


@app.route('/signup', methods=['POST'])
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


@app.route('/blog-post', methods=['POST'])
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

        blog_posts.append(post_data)

        return jsonify({'message': 'Blog post created', 'post': post_data}), 201

    except Exception as e:
        return jsonify({'error': str(e)}), 500

# Route for getting all blog posts


@app.route('/posts', methods=['GET'])
def get_posts():
    try:
        return jsonify({'posts': blog_posts}), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

# Route for getting a single blog post by id


@app.route('/post/<id>', methods=['GET'])
def get_post(id):
    try:
        # Find the post with the given ID
        post = next((post for post in blog_posts if post['id'] == id), None)
        if post:
            return jsonify({'post': post}), 200
        else:
            return jsonify({'error': 'Post not found'}), 404
    except Exception as e:
        return jsonify({'error': str(e)}), 500

# Route for updating a single blog post by id


@app.route('/post/<id>', methods=['PUT'])
def update_post(id):
    try:
        data = request.get_json()
        title = data.get('title')
        content = data.get('content')

        # Find the post with the given ID
        post = next((post for post in blog_posts if post['id'] == id), None)

        if not post:
            return jsonify({'error': 'Post not found'}), 404

        # Update the post with the new data
        post['title'] = title
        post['content'] = content
        return jsonify({'message': 'Blog post updated', 'post': post}), 200

    except Exception as e:
        return jsonify({'error': str(e)}), 500

# Route for deleting a single blog post by id


@app.route('/post/<id>', methods=['DELETE'])
def delete_post(id):
    try:
        # Find the index of the post with the given ID
        index = next((i for i, post in enumerate(
            blog_posts) if post['id'] == id), None)

        if index is not None:
            deleted_post = blog_posts.pop(index)
            return jsonify({'message': 'Blog post deleted', 'post': deleted_post}), 200
        else:
            return jsonify({'error': 'Post not found'}), 404

    except Exception as e:
        return jsonify({'error': str(e)}), 500


if __name__ == '__main__':
    app.run(debug=False)
