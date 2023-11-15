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

    @abstractmethod
    def getUserName(self):
        pass


class ValidUser(User):
    @staticmethod
    def find_user(email, password):
        doc_data = Auth.find_one({"email": email, "password": password})
        if doc_data:
            user = ValidUser(doc_data['_id'], doc_data['name'],
                             doc_data['email'], doc_data['password'])
            return user
        else:
            return False

    def getUserName(self):
        return self.name


class UserNameGetter(ABC):
    @staticmethod
    def Validate(email, password):
        user = ValidUser.findUser(email, password)
        if user:
            return user.getUserName()
        else:
            return None
