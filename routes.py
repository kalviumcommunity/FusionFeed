import os
from pymongo import MongoClient
from flask import Flask, request, jsonify
from auth import AuthValidation

app = Flask(__name__)
blog_posts = []  # A list to store blog posts

# MongoDB initialization

MONGO = os.getenv('MONGO')
Auth = MongoClient(MONGO).test["OOPs"]


class Template:
    def create_data(self, **data):
        pass


class Document(Template):
    def create_data(self, name, email, password):
        doc_data = {"name": name, "email": email, "password": password}
        return doc_data


class BlogPost(Template):
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

        document = Document()
        doc_data = document.create_data(name, email, password)

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

        blog_post = BlogPost()
        post_data = blog_post.create_data(title, content, author)

        blog_posts.append(post_data)

        return jsonify({'message': 'Blog post created', 'post': post_data}), 201

    except Exception as e:
        return jsonify({'error': str(e)}), 500

# Route for getting all blog posts


@app.route('/posts', methods=['GET'])
def get_posts():
    try:
        posts = BlogPost.get_all()
        return jsonify({'posts': posts}), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500


# Route for getting a single blog post by id


@app.route('/post/<id>', methods=['GET'])
def get_post(id):
    try:
        post = BlogPost.get_one(id)
        return jsonify({'post': post}), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

# Route for updating a single blog post by id


@app.route('/post/<id>', methods=['PUT'])
def update_post(id):
    try:
        posttoUpdate = BlogPost.get_one(id)
        data = request.get_json()
        title = data.get('title')
        content = data.get('content')
    # update the post with the new data
        posttoUpdate.update(title, content)
        return jsonify({'message': 'Blog post updated', 'post': posttoUpdate}), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

# Route for deleting a single blog post by id


@app.route('/post/<id>', methods=['DELETE'])
def delete_post(id):
    try:
        posttoDelete = BlogPost.get_one(id)
        posttoDelete.delete()
        return jsonify({'message': 'Blog post deleted', 'post': posttoDelete}), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500


if __name__ == '__main__':
    app.run(debug=True)
