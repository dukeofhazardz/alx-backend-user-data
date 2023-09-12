#!/usr/bin/env python3
"""The Auth module
"""
import bcrypt
from user import User
from sqlalchemy.orm.exc import NoResultFound
from db import DB
from uuid import uuid4


def _hash_password(password: str) -> bytes:
    """A method that takes in a password string argument and returns bytes.
    """
    passwd_hash = bcrypt.hashpw(password.encode("utf-8"), bcrypt.gensalt())
    return passwd_hash


def _generate_uuid() -> str:
    """Returns a string representation of a new UUID.
    """
    return str(uuid4())


class Auth:
    """Auth class to interact with the authentication database.
    """
    def __init__(self):
        """Initializes an instance of the Auth Class
        """
        self._db = DB()

    def register_user(self, email: str, password: str) -> User:
        """Registers user
        """
        try:
            self._db.find_user_by(email=email)
            raise ValueError("User {} already exists".format(email))
        except NoResultFound:
            hashed_pw = _hash_password(password)
            user_obj = self._db.add_user(email, hashed_pw)
            return user_obj

    def valid_login(self, email: str, password: str) -> User:
        """Validates user credentials
        """
        try:
            user = self._db.find_user_by(email=email)
        except NoResultFound:
            return False
        return bcrypt.checkpw(password.encode("utf-8"), user.hashed_password)

    def create_session(self, email: str) -> str:
        """Returns the session ID as a string.
        """
        try:
            user = self._db.find_user_by(email=email)
        except NoResultFound:
            return None
        user.session_id = _generate_uuid()
        return user.session_id

    def get_user_from_session_id(self, session_id: str) -> User | None:
        """Returns the corresponding user of a session_id
        """
        if session_id is None:
            return None
        try:
            user = self._db.find_user_by(session_id=session_id)
        except NoResultFound:
            return None
        return user

    def destroy_session(self, user_id: int) -> None:
        """Updates the corresponding user session ID to None
        """
        try:
            user = self._db.find_user_by(id=user_id)
        except NoResultFound:
            return None
        user.session_id = None

    def get_reset_password_token(self, email: str) -> str:
        """Generates a UUID and update the user reset_token database field
        """
        try:
            user = self._db.find_user_by(email=email)
            user.reset_token = _generate_uuid()
            return user.reset_token
        except NoResultFound:
            raise ValueError

    def update_password(self, reset_token: str, password: str) -> None:
        """Hashes the password and updates the user hashed_password field with
        the new hashed password and the reset_token field to None.
        """
        try:
            user = self._db.find_user_by(reset_token=reset_token)
            user.hashed_password = _hash_password(password)
            user.reset_token = None
        except NoResultFound:
            raise ValueError
