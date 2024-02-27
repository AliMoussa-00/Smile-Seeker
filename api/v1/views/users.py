"""users api endpoints"""
from flask import jsonify, abort

from api.v1.views import app_views
from models import storage


@app_views.route('/users', methods=['GET'], strict_slashes=False)
def get_users():
    """get all users"""
    all_users = storage.all("Users")
    users = []
    if all_users:
        for user in all_users.values():
            users.append(user.to_dict())

    return jsonify(users)


@app_views.route('/users/<user_id>', methods=['GET'], strict_slashes=False)
def get_user(user_id):
    """get a user"""
    user = storage.get("Users", user_id)
    if not user:
        abort(404)
    return jsonify(user.to_dict())
