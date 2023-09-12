#!/usr/bin/env python3
"""The App module
"""

from flask import (Flask, jsonify, request, abort,
                   make_response, redirect, url_for)
from auth import Auth

AUTH = Auth()
app = Flask(__name__)


@app.route("/", methods=["GET"], strict_slashes=False)
def home() -> str:
    """Returns jsonified Page saying 'Bienvenue'
    """
    return jsonify({"message": "Bienvenue"})


@app.route("/users", methods=["POST"], strict_slashes=False)
def users() -> str:
    """Registers a user and returns jsonified Page
    """
    email = request.form['email']
    password = request.form['password']
    if not email or not password:
        return None
    try:
        AUTH.register_user(email, password)
        return jsonify({"email": email, "message": "user created"})
    except ValueError:
        return jsonify({"message": "email already registered"}), 400


@app.route("/sessions", methods=["POST"], strict_slashes=False)
def login() -> str:
    """Creates a new session for the user
    """
    email = request.form['email']
    password = request.form['password']
    if not email or not password:
        return None
    if AUTH.valid_login(email, password) is False:
        return abort(401)
    else:
        session_cookie = AUTH.create_session(email)
        user_session = make_response(jsonify({"email": email,
                                              "message": "logged in"}), 200)
        user_session.set_cookie("session_id", session_cookie)
        return user_session


@app.route("/logout", methods=["DELETE"], strict_slashes=False)
def logout() -> str:
    """Destroys the session and redirect the user to GET /
    """
    session_cookie = request.cookies["session_id"]
    user = AUTH.get_user_from_session_id(session_cookie)
    if user:
        AUTH.destroy_session(user.id)
        return redirect(url_for(home))
    return abort(403)


@app.route("/profile", methods=["GET"], strict_slashes=False)
def profile() -> str:
    """Returns the user profile
    """
    session_cookie = request.cookies["session_id"]
    user = AUTH.get_user_from_session_id(session_cookie)
    if user:
        return make_response(jsonify({"email": user.email}), 200)
    return abort(403)


@app.route("/reset_password", methods=["POST"], strict_slashes=False)
def get_reset_password_token() -> str:
    """Generate a token and responds with reset token
    """
    email = request.form['email']
    if not email:
        return None
    try:
        reset_token = AUTH.get_reset_password_token(email)
        return make_response(jsonify({"email": email,
                                      "reset_token": reset_token}), 200)
    except ValueError:
        return abort(403)


@app.route("/reset_password", methods=["PUT"], strict_slashes=False)
def update_password() -> str:
    """Generate a token and responds with reset token
    """
    email = request.form['email']
    reset_token = request.form['reset_token']
    new_password = request.form['new_password']
    if email is None or reset_token is None or new_password is None:
        return None
    try:
        AUTH.update_password(reset_token, new_password)
        return make_response(jsonify({"email": email,
                                      "message": "Password updated"}), 200)
    except ValueError:
        return abort(403)


if __name__ == "__main__":
    app.run(host="0.0.0.0", port="5000")
