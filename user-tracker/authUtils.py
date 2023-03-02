import datetime
import jwt
from flask_bcrypt import Bcrypt
from flask_jwt_extended import create_access_token

bcrypt = Bcrypt()


class AuthUtils:
    @staticmethod
    def get_pass_hash(password):
        return bcrypt.generate_password_hash(password.encode('utf-8'), 10)

    @staticmethod
    def check_pass_hash(hash, password):
        return bcrypt.check_password_hash(hash, password)

    @staticmethod
    def decode_auth_token(auth_token):
        try:
            payload = jwt.decode(auth_token, 'ghghutt')
            return payload['sub']
        except jwt.ExpiredSignatureError:
            return 'Signature expired. Please log in again.'
        except jwt.InvalidTokenError:
            return 'Invalid token. Please log in again.'

    @staticmethod
    def encode_auth_token(user_id):
        try:
            return create_access_token(user_id)
        except Exception as e:
            return e
