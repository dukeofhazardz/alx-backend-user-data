#!/usr/bin/env python3
""" Module of SessionExpAuth Class
"""
from api.v1.auth.session_auth import SessionAuth
from datetime import datetime, timedelta
from typing import TypeVar
from models.user import User
import os


class SessionExpAuth(SessionAuth):
    """ The SessionExpAuth Class """
    def __init__(self):
        """ Initializes the SessionExpAuth Class """
        if not os.getenv("SESSION_DURATION") or not isinstance(
                int(os.getenv("SESSION_DURATION")), int):
            self.session_duration = 0
        self.session_duration = int(os.getenv("SESSION_DURATION"))

    def create_session(self, user_id=None):
        """ A method that creates the session """
        session_id = super().create_session(user_id)
        if not session_id:
            return None
        session_dictionary = {"user_id": user_id,
                              "created_at": datetime.now()}
        self.user_id_by_session_id[session_id] = session_dictionary
        return session_id

    def user_id_for_session_id(self, session_id=None):
        """ A method that returns user_id from the session dictionary """
        if session_id is None or session_id not in \
                self.user_id_by_session_id.keys():
            return None
        session_dict = self.user_id_by_session_id[session_id].get(
            "session_dictionary")
        if self.session_duration <= 0:
            return session_dict.get("user_id")

        if "created_at" not in session_dict.keys():
            return None

        if session_dict.get("created_at") + timedelta(
                seconds=self.session_duration) >= datetime.now():
            return None

        return session_dict.get("user_id")
