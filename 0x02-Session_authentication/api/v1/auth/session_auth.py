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
