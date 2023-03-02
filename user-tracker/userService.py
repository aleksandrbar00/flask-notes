from user import User
from db import db
from authUtils import AuthUtils


class UserService:
    @staticmethod
    def create(payload):
        user = User(
            username=payload['username'],
            password=AuthUtils.get_pass_hash(payload['password']).decode('utf-8')
        )
        db.session.add(user)
        db.session.commit()

    @staticmethod
    def get_user_info(id):
        return db.get_or_404(User, id)

    @staticmethod
    def get_user_by_username(username):
        return db.session.query(User).filter_by(username=username).one()
