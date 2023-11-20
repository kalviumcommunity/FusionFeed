from src.models.user_model import User
from src.models.auth_middleware import UserAuthenticator

class AuthValidation:
    @staticmethod
    def Validate(email, password):
        user = UserAuthenticator.find_user(email, password)
        return user.get_user_name() if user else False
