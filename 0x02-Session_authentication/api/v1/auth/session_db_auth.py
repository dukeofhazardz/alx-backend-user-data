#!/usr/bin/env python3
""" Module of SessionDBAuth Class
"""
from api.v1.auth.session_exp_auth import SessionExpAuth
from models.user_session import UserSession
import os


class SessionDBAuth(SessionExpAuth):
    """ The SessionDBAuth Class """
    def create_session(self, user_id=None):
        """ A method that creates and stores new instance of UserSession
        Return:
            The Session ID
        """
        session_id = super().create_session(user_id)
        user_session = UserSession(user_id, session_id)
        user_session.save_to_file()
        return session_id

    def user_id_for_session_id(self, session_id=None):
        """ A method that returns the User ID by requesting UserSession in
            the database based on session_id """
        user_session = UserSession()
        user = user_session.search({"session_id": session_id})
        return user[0].user_id

    def destroy_session(self, request=None):
        """ A method that destroys the UserSession based on the Session ID
            from the request cookie """
        session_id = self.session_cookie(request)

        if session_id:
            user_session = user_session.search({"session_id": session_id})[0]
            if user_session:
                user_session.remove()
