from flask import Flask
from pymongo import MongoClient
import os
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)

# Configuration
MONGO = os.getenv('MONGO')
client = MongoClient(MONGO)
db = client.test
Auth = db["OOPs"]
Blogs = db["Blog"]

# Class for representing a blog post


class BlogPost:
    def __init__(self, title, content, author):
        self.title = title
        self.content = content
        self.author = author

    def to_dict(self):
        return {"title": self.title, "content": self.content, "author": self.author}


# Create an array of blog posts
blog_posts = []

# Debug
if __name__ == '__main__':
    app.run(debug=True)
