#!/usr/bin/env python3
""" Module of Auth Class
"""
from api.v1.auth.auth import Auth
import base64
from typing import TypeVar
from models.user import User


class BasicAuth(Auth):
    """ The BasicAuth Class that inherits from the Auth Class """
    def extract_base64_authorization_header(self,
                                            authorization_header: str) -> str:
        """ A method that returns the Base64 part of the Authorization
            header for a Basic Authentication """
        if authorization_header is None or not isinstance(authorization_header,
                                                          str):
            return None

        if not authorization_header.startswith('Basic '):
            return None

        return authorization_header[len("Basic "):]

    def decode_base64_authorization_header(self,
                                           base64_authorization_header:
                                           str) -> str:
        """ A method that returns the decoded value of a
            Base64 string base64_authorization_header """
        if base64_authorization_header is None:
            return None

        if not isinstance(base64_authorization_header, str):
            return None
        try:
            base64_decoded = base64.b64decode(base64_authorization_header)
            utf_decoded = base64_decoded.decode('utf-8')
        except (base64.binascii.Error, UnicodeDecodeError):
            return None

        return utf_decoded

    def extract_user_credentials(self,
                                 decoded_base64_authorization_header:
                                 str) -> (str, str):
        """ A method that returns the user email and password from the
            Base64 decoded value """
        if decoded_base64_authorization_header is None:
            return None, None

        if not isinstance(decoded_base64_authorization_header, str):
            return None, None

        if ':' not in decoded_base64_authorization_header:
            return None, None

        t: tuple = decoded_base64_authorization_header.split(':')
        return t[0], t[1]

    def user_object_from_credentials(self,
                                     user_email: str,
                                     user_pwd: str) -> TypeVar('User'):
        """ A method that returns the User instance based on his
            email and password """
        if user_email is None or not isinstance(user_email, str):
            return None

        if user_pwd is None or not isinstance(user_pwd, str):
            return None

        users = User().search({'email': f'{user_email}'})
        if users:
            for each_user in users:
                if each_user.is_valid_password(user_pwd):
                    return each_user
                return None
            return None

    def current_user(self, request=None) -> TypeVar('User'):
        """ A method that overloads Auth and retrieves the User
            instance for a request """
        authorization_header = self.authorization_header(request)
        if authorization_header is None or \
                not authorization_header.startswith('Basic '):
            return None

        base64_auth = self.extract_base64_authorization_header(
            authorization_header)
        if base64_auth is None:
            return None

        decoded_auth = self.decode_base64_authorization_header(base64_auth)
        if decoded_auth is None:
            return None

        user_credentials = self.extract_user_credentials(decoded_auth)
        if user_credentials is None:
            return None

        return self.user_object_from_credentials(*user_credentials)
