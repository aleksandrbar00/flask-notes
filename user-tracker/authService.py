from userService import UserService
from authUtils import AuthUtils
from db import db


class AuthService:
    @staticmethod
    def login_user(payload):
        try:
            user = UserService.get_user_by_username(payload['username'])
            token = AuthUtils.encode_auth_token(user.id)

            if not AuthUtils.check_pass_hash(user.password, payload['password']):
                return 'Credentials doesnt match', 400

            return token, 200

        except db.exc.NoResultFound:
            return 'User not found', 404
