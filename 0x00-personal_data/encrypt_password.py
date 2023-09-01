#!/usr/bin/env python3
""" Password Encryption """
import bcrypt
from typing import Literal


def hash_password(password: str) -> bytes:
    """ A function that returns a salted, hashed password,
        which is a byte string. """
    password_bytes: bytes = password.encode('utf-8')
    hashed_pw: bytes = bcrypt.hashpw(password_bytes, bcrypt.gensalt())
    return hashed_pw


def is_valid(hashed_password: bytes,
             password: str) -> Literal[True] | Literal[False]:
    """ A function that validates that the provided password
        matches the hashed password. """
    password_bytes: bytes = password.encode('utf-8')
    pw_status = bcrypt.checkpw(password_bytes, hashed_password)
    if pw_status:
        return True
    return False
