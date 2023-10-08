from flask import Flask, request, jsonify
from pymongo import MongoClient
import os
from dotenv import load_dotenv
from auth import AuthValidation

load_dotenv()

app = Flask(__name__)

# Configuration
MONGO = os.getenv('MONGO')
client = MongoClient(MONGO)
db = client.test
Auth = db["OOPs"]
Blogs = db["Blog"]

# Class for representing a blog post


class BlogPost:
    def __init__(self, title, content, author):
        self.title = title
        self.content = content
        self.author = author

    def to_dict(self):
        return {"title": self.title, "content": self.content, "author": self.author}


# Create an array of blog posts
blog_posts = []

# Classes and Objects


class Document:

    # Constructor
    def __init__(self, name, email, password):
        self.name = name
        self.email = email
        self.password = password
        print(f"Document object created for {self.name}")

    # Destructor
    def __del__(self):
        print(f"Document object destroyed for {self.name}")


"""This Route is for creating a new user"""


@app.route('/signup', methods=['POST'])
def create_document():
    try:
        data = request.get_json()
        name = data.get('name')
        email = data.get('email')
        password = data.get('password')

        if not (name and email and password):
            return jsonify({'error': 'Missing data'}), 400

        # Create an instance of the Document class
        new_doc = Document(name, email, password)
        doc_data = {"name": new_doc.name,
                    "email": new_doc.email, "password": new_doc.password}

        # Insert the document into the collection
        result = Auth.insert_one(doc_data)
        return jsonify({'message': 'Document created', 'document_id': str(result.inserted_id)}), 201

    except Exception as e:
        return jsonify({'error': str(e)}), 500


"""This Route is for creating a new blog post"""


@app.route('/blog-post', methods=['POST'])
def create_post():
    try:
        data = request.get_json()
        email = request.headers.get('email')
        password = request.headers.get('password')

        if not (email and password):
            return jsonify({'error': 'Missing email or password headers'}), 400

        # Use the static method to get the user's name
        author_name = AuthValidation.Validate(email, password)

        if not author_name:
            return jsonify({'error': 'Invalid email or password'}), 401

        title = data.get('title')
        content = data.get('content')

        if not (title and content):
            return jsonify({'error': 'Missing title or content'}), 400

        # Create a new blog post
        new_post = BlogPost(title, content, author_name)

        # Add the new post to the array of blog posts
        blog_posts.append(new_post)

        return jsonify({'message': 'Post created'}), 201

    except Exception as e:
        return jsonify({'error': str(e)}), 500


"""This Route is for getting all blog posts"""


@app.route('/posts', methods=['GET'])
def get_posts():
    pass


"""This Route is for getting a single blog post by id"""


@app.route('/post/<id>', methods=['GET'])
def get_post(id):
    pass


"""This Route is for updating a single blog post by id"""


@app.route('/post/<id>', methods=['PUT'])
def update_post(id):
    pass


"""This Route is for deleting a single blog post by id"""


@app.route('/post/<id>', methods=['DELETE'])
def delete_post(id):
    pass


# debug
if __name__ == '__main__':
    app.run(debug=True)
