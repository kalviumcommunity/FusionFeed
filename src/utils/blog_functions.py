from flask import jsonify, request
from src.models.doc_model import BlogPostHandler
from src.middlewares.auth_mid import AuthValidation


blog_posts = []  



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

def get_posts():
    try:
        return jsonify({'posts': blog_posts}), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

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
