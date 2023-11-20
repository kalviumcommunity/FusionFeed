from abc import ABC, abstractmethod

class User(ABC):
    def __init__(self, _id, name, email, password):
        self._id = _id
        self._name = name
        self._email = email
        self._password = password

    @abstractmethod
    def get_user_name(self):
        pass
