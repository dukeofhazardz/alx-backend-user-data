#!/usr/bin/env python3
"""
Main file
"""
import requests
'''# 0
from user import User

print(User.__tablename__)

for column in User.__table__.columns:
    print("{}: {}".format(column, column.type))


# 1
from db import DB
from user import User

my_db = DB()

user_1 = my_db.add_user("test@test.com", "SuperHashedPwd")
print(user_1.id)
print(user_1.email)

user_2 = my_db.add_user("test1@test.com", "SuperHashedPwd1")
print(user_2.id)
print(user_2.email)


# 2
from sqlalchemy.exc import InvalidRequestError
from sqlalchemy.orm.exc import NoResultFound


my_db = DB()

user = my_db.add_user("test@test.com", "PwdHashed")
print(user.id)

find_user = my_db.find_user_by(email="test@test.com")
print(find_user.id)

try:
    find_user = my_db.find_user_by(email="test2@test.com")
    print(find_user.id)
except NoResultFound:
    print("Not found")

try:
    find_user = my_db.find_user_by(no_email="test@test.com")
    print(find_user.id)
except InvalidRequestError:
    print("Invalid")


# 3
my_db = DB()

email = 'test@test.com'
hashed_password = "hashedPwd"

user = my_db.add_user(email, hashed_password)
print(user.id)

try:
    my_db.update_user(user.id, hashed_password='NewPwd')
    print("Password updated")
except ValueError:
    print("Error")


# 4
from auth import _hash_password

print(_hash_password("Hello Holberton"))


# 5
from auth import Auth

email = 'me@me.com'
password = 'mySecuredPwd'

auth = Auth()

try:
    user = auth.register_user(email, password)
    print("successfully created a new user!")
except ValueError as err:
    print("could not create a new user: {}".format(err))

try:
    user = auth.register_user(email, password)
    print("successfully created a new user!")
except ValueError as err:
    print("could not create a new user: {}".format(err))


# 8
from auth import Auth

email = 'bob@bob.com'
password = 'MyPwdOfBob'
auth = Auth()

auth.register_user(email, password)

print(auth.valid_login(email, password))

print(auth.valid_login(email, "WrongPwd"))

print(auth.valid_login("unknown@email", password))


# 9
from auth import Auth

email = 'bob@bob.com'
password = 'MyPwdOfBob'
auth = Auth()

auth.register_user(email, password)

print(auth.create_session(email))
print(auth.create_session("unknown@email.com"))'''


# main
EMAIL = "guillaume@holberton.io"
PASSWD = "b4l0u"
NEW_PASSWD = "t4rt1fl3tt3"


def register_user(email: str, password: str) -> None:
    """Assert for register_user
    """
    response = requests.post("http://127.0.0.1:5050/users",
                             data={'email': email, 'password': password})
    assert response.status_code == 200


def log_in_wrong_password(email: str, password: str) -> None:
    """Assert for log_in_wrong_password
    """
    response = requests.post("http://127.0.0.1:5050/sessions",
                             data={'email': email, 'password': password})
    assert response.status_code == 401


def log_in(email: str, password: str) -> str:
    """Assert for log_in
    """
    response = requests.post("http://127.0.0.1:5050/sessions",
                             data={'email': email, 'password': password})
    assert response.status_code == 200


def profile_unlogged() -> None:
    """Assert for profile_unlogged
    """
    response = requests.post("http://127.0.0.1:5050/sessions")
    assert response.status_code == 400


def profile_logged(session_id: str) -> None:
    """Assert for profile_logged
    """
    response = requests.get("http://127.0.0.1:5050/profile",
                            data={'session_id': session_id})
    assert response.status_code == 200


def log_out(session_id: str) -> None:
    """Assert for log_out
    """
    response = requests.delete("http://127.0.0.1:5050/logout",
                               data={'session_id': session_id})
    assert response.status_code == 302


def reset_password_token(email: str) -> str:
    """Assert for reset_password_token
    """
    response = requests.delete("http://127.0.0.1:5050/reset_password",
                               data={'email': email})
    assert response.status_code == 200


def update_password(email: str, reset_token: str, new_password: str) -> None:
    """Assert for update_password
    """
    response = requests.put("http://127.0.0.1:5050/reset_password",
                            data={'email': email,
                                  'reset_token': reset_token,
                                  'new_password': new_password})
    assert response.status_code == 200


if __name__ == "__main__":

    register_user(EMAIL, PASSWD)
    log_in_wrong_password(EMAIL, NEW_PASSWD)
    profile_unlogged()
    session_id = log_in(EMAIL, PASSWD)
    profile_logged(session_id)
    log_out(session_id)
    reset_token = reset_password_token(EMAIL)
    update_password(EMAIL, reset_token, NEW_PASSWD)
    log_in(EMAIL, NEW_PASSWD)
