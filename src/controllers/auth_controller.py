from flask import request, Response, json, Blueprint
from pymongo import MongoClient
import os


MONGO = os.getenv('MONGO')
Auth = MongoClient(MONGO).test["OOPs"]

# Route Functions
from src.routes.user_functions import create_document , create_post

# user controller blueprint to be registered with api blueprint
app = Blueprint("users", __name__)
