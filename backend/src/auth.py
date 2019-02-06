from typing import Union, Sequence, List, Optional
from backend.src.model.mysql import db, User, Tracker, TrackerUserLink
from backend.src.helpers import StringHelper
from flask import request, Response
from functools import wraps
import datetime
from hashlib import md5, sha256


class Auth:
    @classmethod
    def add_new_user(cls, login, hash, redmine_token=None):
        user = cls.get_user_by_login(login)
        if user is not None:
            return None
        token_len = User.token.property.columns[0].type.length >> 3
        user = User(login=login, hash=hash, token=StringHelper.get_random_ascii_string(token_len))

        # todo привязку стоит оформить явно, через фронт и отдельный метод
        tracker_redmine = db.session.query(Tracker).filter(Tracker.title == 'redmine').first()
        tracker_evo = db.session.query(Tracker).filter(Tracker.title == 'evolution').first()

        if redmine_token is not None:
            from .model.trackers.redmine import Redmine
            redmine = Redmine(tracker_redmine.api_url, token=redmine_token)
            external_user_id = redmine.get_user_id()
            tracker_link = TrackerUserLink(tracker=tracker_redmine, user=user, external_api_key=redmine_token, external_user_id=external_user_id)
        else:
            tracker_link = TrackerUserLink(tracker=tracker_redmine, user=user)

        tracker_link2 = TrackerUserLink(tracker=tracker_evo, user=user)

        db.session.add(tracker_link)
        db.session.add(tracker_link2)
        db.session.add(user)
        db.session.commit()
        return user

    @staticmethod
    def get_user_by_token(token) -> Optional[User]:
        return db.session.query(User).filter(User.token == token).first()

    @staticmethod
    def get_user_by_login(login) -> Optional[User]:
        return db.session.query(User.id).filter(User.login == login).first()

    @staticmethod
    def get_user_by_id(user_id) -> Optional[User]:
        return db.session.query(User).filter(User.id == user_id).first()

    @staticmethod
    def get_user_by_login_and_hash(login, hash) -> Optional[User]:
        return db.session.query(User.id, User.token).filter(User.login == login).filter(User.hash == hash).first()

    @classmethod
    def get_request_token(cls) -> Optional[str]:
        return request.headers.get('token')

    @classmethod
    def get_request_user(cls) -> Optional[User]:
        return db.session.query(User).filter(User.token == cls.get_request_token()).first()

    @classmethod
    def get_hash(cls, login, password, salt) -> Optional[str]:
        return sha256(
            md5(password.encode() + salt).hexdigest().encode() +
            md5(login.encode() + salt).hexdigest().encode()
        ).hexdigest()

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
            # db.session.add(user)
            result = func(*args, **kwargs)
            # sqlalchemy при старте открывает транзакцию с БД
            # этот коммит её закрывает - внутри ядра коммиты можно не ставить(если айдишники изменений не нужны),
            # чтобы все изменения упали в одну транзакцию на запрос
            # !!! работает только для методов, обернутых декоратором @Auth.check_api_request
            # здесь же пилить функционал глобального rollback, только в result пробросить error, и тут отловить
            db.session.commit()
            return result

        return argument_router

    @classmethod
    def check_api_request_readonly(cls, func):
        @wraps(func)
        def argument_router(*args, **kwargs):
            token = cls.get_request_token()
            user = None  # type:User
            if token is not None:
                user = cls.get_user_by_token(token)
            if user is None:
                return Response(status=401)

            result = func(*args, **kwargs)
            return result

        return argument_router
