from flask import Flask, request, jsonify
from pymongo import MongoClient
import os
from dotenv import load_dotenv


load_dotenv()
MONGO = os.getenv('MONGO')

client = MongoClient(MONGO)

db = client.test
collection = db["OOPs"]


app = Flask(__name__)

@app.route('/add', methods=['POST'])
def create_database():
    try:
        new_doc = {"name": "A", "age": 18}
        result = collection.insert_one(new_doc)
        return str(result.inserted_id), 200
    
    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)