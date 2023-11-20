from flask import Blueprint
from src.controllers.auth_controller import app

api = Blueprint('api', __name__)

api.register_blueprint(app)