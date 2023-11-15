from pymongo import MongoClient
import os
from abc import ABC, abstractmethod

MONGO = os.getenv('MONGO')
Auth = MongoClient(MONGO).test["OOPs"]

# static Validation class for validating the user


class User(ABC):
    def __init__(self, _id, name, email, password):
        self._id = _id
        self._name = name
        self._email = email
        self._password = password

    def get_id(self):
        return self._id

    def get_name(self):
        return self._name

    def get_email(self):
        return self._email

    def get_password(self):
        return self._password


class UserAuthenticator:
    @staticmethod
    def find_user(email, password):
        doc_data = Auth.find_one({"email": email, "password": password})
        if doc_data:
            user = User(doc_data['_id'], doc_data['name'],
                        doc_data['email'], doc_data['password'])
            return user
        else:
            return None


class UserNameGetter(ABC):
    @staticmethod
    @abstractmethod
    def get_user_name(user):
        if user:
            return user.get_name()
        else:
            return None


class UserNameGetter(ABC):
    @staticmethod
    def validate(email, password):
        user = UserAuthenticator.find_user(email, password)
        return UserNameGetter.get_user_name(user)

