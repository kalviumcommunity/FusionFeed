from abc import ABC, abstractmethod

class DataHandler(ABC):
    @abstractmethod
    def create_data(self, **data):
        pass


class DocumentHandler(DataHandler):
    def create_data(self, name, email, password):
        doc_data = {"name": name, "email": email, "password": password}
        return doc_data


class BlogPostHandler(DataHandler):
    def create_data(self, title, content, author):
        post_data = {"title": title, "content": content, "author": author}
        return post_data