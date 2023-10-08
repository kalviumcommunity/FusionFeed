from flask import request, jsonify
from app import app, db, Auth, BlogPost, blog_posts
from auth import AuthValidation

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

# Route for creating a new user
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

# Route for creating a new blog post
@app.route('/blog-post', methods=['POST'])
def create_post():
    # (Your existing route code for creating blog posts)
    pass

# Route for getting all blog posts
@app.route('/posts', methods=['GET'])
def get_posts():
    pass

# Route for getting a single blog post by id
@app.route('/post/<id>', methods=['GET'])
def get_post(id):
    pass

# Route for updating a single blog post by id
@app.route('/post/<id>', methods=['PUT'])
def update_post(id):
    pass

# Route for deleting a single blog post by id
@app.route('/post/<id>', methods=['DELETE'])
def delete_post(id):
    pass
