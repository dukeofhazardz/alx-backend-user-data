#!/usr/bin/env python3
""" Module of SessionAuth Class
"""
from api.v1.auth.auth import Auth
from typing import TypeVar
from models.user import User
from uuid import uuid4


class SessionAuth(Auth):
    """ The SessionAuth Class """
    user_id_by_session_id = {}

    def create_session(self, user_id: str = None) -> str:
        """ A method that creates a Session ID for a user_id:
        Return:
            None if user_id is None
            None if user_id is not a string
            The Session ID
        """
        if user_id and isinstance(user_id, str):
            session_id = str(uuid4())
            self.user_id_by_session_id[session_id] = user_id

            return session_id
        return None

    def user_id_for_session_id(self, session_id: str = None) -> str:
        """ A method that returns a User ID based on a Session ID
        Return:
            None if session_id is None
            None if session_id is not a string
            The value (the User ID) for the key session_id in the dictionary
            user_id_by_session_id.
        """
        if not session_id or not isinstance(session_id, str):
            return None
        user_id = self.user_id_by_session_id.get(session_id)
        return user_id

    def current_user(self, request=None):
        """ A method that returns a User instance based on a cookie value
        Return:
            User instance based on the cookie _my_session_id
        """
        cookie = self.session_cookie(request)
        user_id = self.user_id_by_session_id.get(cookie)
        user = User().get(user_id)
        return user

    def destroy_session(self, request=None):
        """ A method that deletes the user session / logout """
        if request is None:
            return None
        if self.session_cookie(request) is None:
            return False
        if self.user_id_for_session_id(self.session_cookie(request)) is None:
            return False

        del self.user_id_by_session_id[self.session_cookie(request)]
        return True
