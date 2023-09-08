#!/usr/bin/env python3
""" Module of Session Auth views
"""
from api.v1.views import app_views
from flask import abort, jsonify, request
from models.user import User
import os


@app_views.route('/auth_session/login', methods=['POST'], strict_slashes=False)
def authenticate_login() -> str:
    """ Authenticates the login session """
    email = request.form.get('email')
    if not email:
        return jsonify({"error": "email missing"}), 400

    password = request.form.get('password')
    if not password:
        return jsonify({"error": "password missing"}), 400

    user = User().search({'email': f'{email}'})
    if not user:
        return jsonify({"error": "no user found for this email"}), 404

    if not user[0].is_valid_password(password):
        return jsonify({"error": "wrong password"}), 401

    from api.v1.auth.session_auth import SessionAuth
    auth = SessionAuth()
    session_id = auth.create_session(user[0].id)
    cookie_name = os.getenv("SESSION_NAME")
    user_response = jsonify(user[0].to_json())
    user_response.set_cookie(cookie_name, session_id)

    return user_response
