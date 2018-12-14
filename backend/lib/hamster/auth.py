from backend.lib.hamster.model import db, User
from backend.lib.helpers import StringHelper
from flask import request, jsonify
from functools import wraps

auth_path = 'auth'


class Auth:
    def __init__(self, redirect_path):
        self.redirect_path = redirect_path

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
        return db.session.query(User.id).filter(User.token == token).first()

    @staticmethod
    def get_login_id(login):
        return db.session.query(User.id).filter(User.login == login).first()

    @classmethod
    def check_api_request(cls, func):
        @wraps(func)
        def argument_router(*args, **kwargs):
            token = request.headers.get('token')
            if token is not None:
                user_id = cls.get_token_id(token)
            if user_id is None:
                return jsonify({'redirect': auth_path})
            return func(*args, **kwargs)

        return argument_router
