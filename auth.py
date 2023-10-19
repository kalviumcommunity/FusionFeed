from pymongo import MongoClient
import os

MONGO = os.getenv('MONGO')
Auth = MongoClient(MONGO).test["OOPs"]


class User:
    def __init__(self, _id, name, email, password):
        self._id = _id
        self.name = name
        self.email = email
        self.password = password


class isValidUser:
    @staticmethod
    def findUser(email, password):
        doc_data = Auth.find_one({"email": email, "password": password})
        if doc_data:
            user = User(doc_data['_id'], doc_data['name'],
                        doc_data['email'], doc_data['password'])
            return user
        else:
            return None


class getName:
    @staticmethod
    def getUserName(user):
        if user:
            return user.name
        else:
            return None


class AuthValidation:
    @staticmethod
    def Validate(email, password):
        user = isValidUser.findUser(email, password)
        return getName.getUserName(user)
