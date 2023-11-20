from flask import request, Response, json, Blueprint
from pymongo import MongoClient
import os


MONGO = os.getenv('MONGO')
Auth = MongoClient(MONGO).test["OOPs"]

# Route Functions
from src.routes.user_functions import create_document
from src.utils.blog_functions import create_post, get_post , update_post , delete_post , get_posts

# user controller blueprint to be registered with api blueprint
app = Blueprint("users", __name__)

app.route('/signup', methods=['POST'])(create_document)

app.route('/blog-post', methods=['POST'])(create_post)

app.route('/posts', methods=['GET'])(get_posts)

app.route('/post/<id>', methods=['GET'])(get_post)

app.route('/post/<id>', methods=['PUT'])(update_post)

app.route('/post/<id>', methods=['DELETE'])(delete_post)


