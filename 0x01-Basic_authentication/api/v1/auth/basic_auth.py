#!/usr/bin/env python3
""" Module of Auth Class
"""
from api.v1.auth.auth import Auth
import base64


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
        except base64.binascii.Error:
            return None

        return base64_decoded.decode('utf-8')

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
