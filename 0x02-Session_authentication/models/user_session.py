#!/usr/bin/env python3
""" UserSession module
"""
import hashlib
from models.base import Base


class UserSession(Base):
    """ UserSession class
    """
    def __init__(self, *args: list, **kwargs: dict):
        """ Initializes a UserSession instance """
        super().__init__(*args, **kwargs)
        self.user_id: str = kwargs.get('user_id')
        self.session_id: str = kwargs.get('session_id')