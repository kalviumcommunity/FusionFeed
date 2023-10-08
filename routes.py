from flask import request, jsonify
from main import app,  Auth, BlogPost, blog_posts
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
                    "email": new_doc.email,
                    "password": new_doc.password}

        # Insert the document into the collection
        result = Auth.insert_one(doc_data)
        return jsonify({'message': 'Document created', 'document_id': str(result.inserted_id)}), 201

    except Exception as e:
        return jsonify({'error': str(e)}), 500

# Route for creating a new blog post


@app.route('/blog-post', methods=['POST'])
def create_post():

    try:
        data = request.get_json()
        email = request.headers.get('email')
        password = request.headers.get('password')

        if not (email and password):
            return jsonify({'error': 'Missing email or password headers'}), 400

        # Check if the email and password match with the ones stored in the database
        doc_data = AuthValidation.Validate(email, password)

        if not doc_data:
            return jsonify({'error': 'Invalid email or password'}), 401

        title = data.get('title')
        content = data.get('content')
        author = doc_data

        if not (title and content):
            return jsonify({'error': 'Missing title or content'}), 400

        # Create an instance of the BlogPost class
        new_post = BlogPost(title, content, author)

        # Add it to the array
        blog_posts.append(new_post)

        # Send the post to the database
        post_data = new_post.send()

        return jsonify({'message': 'Blog post created', 'post': post_data}), 201

    except Exception as e:
        return jsonify({'error': str(e)}), 500


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


if __name__ == '__main__':
    app.run(debug=True)
