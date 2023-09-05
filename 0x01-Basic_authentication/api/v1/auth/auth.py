#!/usr/bin/env python3
""" Module of Auth Class
"""
from flask import jsonify, abort, request
from typing import List, TypeVar


class Auth:
    """ The Auth Class """
    def require_auth(self, path: str, excluded_paths: List[str]) -> bool:
        """ A public method that returns returns False - path
            and excluded_paths """
        return False

    def authorization_header(self, request=None) -> str:
        """ A public method that returns None - request """
        return None

    def current_user(self, request=None) -> TypeVar('User'):
        """ A public method that returns None - request """
        return None
