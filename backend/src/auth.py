from backend.src.model.mysql import db, User
from backend.src.helpers import StringHelper
from flask import request, Response
from functools import wraps
import datetime


class Auth(object):
    @classmethod
    def add_new_user(cls, login, hash):
        user_id = cls.get_login_id(login)
        if user_id is not None:
            return None
        token_len = User.token.property.columns[0].type.length >> 3
        user = User(login=login, hash=hash, token=StringHelper.get_random_ascii_string(token_len))
        db.session.add(user)
        return user

    @staticmethod
    def get_user_by_login_and_hash(login, hash):
        return db.session.query(User.id, User.token).filter(User.login == login).filter(User.hash == hash).first()

    @staticmethod
    def get_user_by_token(token):
        return db.session.query(User).filter(User.token == token).first()

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
            user = None  # type:User
            if token is not None:
                user = cls.get_user_by_token(token)
            if user is None:
                return Response(status=401)
            user.last_login = datetime.datetime.now()
            db.session.add(user)
            result = func(*args, **kwargs)
            # sqlalchemy при старте открывает транзакцию с БД
            # этот коммит её закрывает - внутри ядра коммиты можно не ставить(если айдишники изменений не нужны), чтобы все изменения упали в одну транзакцию на запрос
            # здесь же пилить функционал глобального rollback, только в result пробросить error, и тут отловить
            db.session.commit()
            return result

        return argument_router
