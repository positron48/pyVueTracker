from backend.src.model import db, User
from backend.src.helpers import StringHelper
from flask import request, Response
from functools import wraps


class Auth(object):
    @classmethod
    def add_new_user(cls, login, hash):
        user_id = cls.get_login_id(login)
        if user_id is not None:
            return None
        token_len = User.token.property.columns[0].type.length >> 3
        user = User(login=login, hash=hash, token=StringHelper.get_random_ascii_string(token_len))
        db.session.add(user)
        db.session.commit()
        return user

    @staticmethod
    def get_user_by_login_and_hash(login, hash):
        return db.session.query(User.id, User.token).filter(User.login == login).filter(User.hash == hash).first()

    @staticmethod
    def get_token_id(token):
        user = db.session.query(User.id).filter(User.token == token).first()
        return user.id

    @staticmethod
    def get_login_id(login):
        user = db.session.query(User.id).filter(User.login == login).first()
        return user.id

    @classmethod
    def get_request_token(cls):
        return request.headers.get('token')

    @classmethod
    def check_api_request(cls, func):
        @wraps(func)
        def argument_router(*args, **kwargs):
            token = cls.get_request_token()
            user_id = None
            if token is not None:
                user_id = cls.get_token_id(token)
            if user_id is None:
                return Response(status=401)
            return func(*args, **kwargs)

        return argument_router
