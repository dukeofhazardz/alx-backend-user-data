#!/usr/bin/env python3
""" Module of Auth Class
"""
from flask import jsonify, abort, request
from typing import List, TypeVar


class Auth:
    """ The Auth Class """
    def require_auth(self, path: str, excluded_paths: List[str]) -> bool:
        """ A public method that returns True if the path is not in the
            list of strings excluded_paths """
        if path == None or excluded_paths == None or excluded_paths == []:
            return True
        for excluded_path in excluded_paths:
            if not path.endswith('/'):
                path += '/'
            if not excluded_path.endswith('/'):
                excluded_path += '/'
        if path not in excluded_paths:
            return True
        return False

    def authorization_header(self, request=None) -> str:
        """ A public method that returns None - request """
        return None

    def current_user(self, request=None) -> TypeVar('User'):
        """ A public method that returns None - request """
        return None
