import os
from pymongo import MongoClient

MONGO = os.getenv('MONGO')
Auth = MongoClient(MONGO).test["OOPs"]


class AuthValidation:
    @staticmethod
    def Validate(email, password):
        # Check if the email and password match with the ones stored in the database
        doc_data = Auth.find_one({"email": email, "password": password})
        if doc_data:
            return doc_data["name"]
        else:
            return None
