from pymongo import MongoClient
import os

from src.models.user_model import User


MONGO = os.getenv('MONGO')
Auth = MongoClient(MONGO).test["OOPs"]



class UserAuthenticator(User):
    @staticmethod
    def find_user(email, password):
        doc_data = Auth.find_one({"email": email, "password": password})
        if doc_data:
            user = UserAuthenticator(doc_data['_id'], doc_data['name'],
                                     doc_data['email'], doc_data['password'])
            return user
        else:
            return False

    def get_user_name(self):
        return self._name
