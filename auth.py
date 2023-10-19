from pymongo import MongoClient
import os
from abc import ABC, abstractmethod

MONGO = os.getenv('MONGO')
Auth = MongoClient(MONGO).test["OOPs"]


class User(ABC):
    def __init__(self, _id, name, email, password):
        self._id = _id
        self._name = name
        self._email = email
        self._password = password

    @abstractmethod
    def get_user_name(self):
        pass


class UserAuthenticator(User):
    @staticmethod
    def find_user(email, password):
        doc_data = Auth.find_one({"email": email, "password": password})
        if doc_data:
            user = UserAuthenticator(doc_data['_id'], doc_data['name'],
                                     doc_data['email'], doc_data['password'])
            return user
        else:
            return None

    def get_user_name(self):
        return self._name


class AuthValidation:
    @staticmethod
    def validate(email, password):
        user = UserAuthenticator.find_user(email, password)
        return user.get_user_name() if user else None
