"""users api endpoints"""
import hashlib

from flask import jsonify, abort, request, make_response

from api.v1.views import app_views
from models import storage
from models.users import Users


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


@app_views.route('/users', methods=['POST'], strict_slashes=False)
def create_user():
    """create a user object"""
    if not request.get_json():
        abort(404, description="Not Json")
    data = request.get_json()

    user = Users(**data)
    user.save()
    return make_response(jsonify(user.id), 201)


@app_views.route('/log_user', methods=['POST'], strict_slashes=False)
def loginUser():
    """check if user exists to login"""
    if not request.get_json():
        abort(404, description="Not Json")
    data = request.get_json()

    if "email" not in data or "password" not in data:
        abort(404, description="email or password is missing")
    
    hashed_password = hashlib.md5(data['password'].encode('utf-8')).hexdigest()

    user = storage.login(Users, data['email'], hashed_password)
    if user:
        return make_response(jsonify(user.to_dict()), 201)
    else:
        return make_response("not registered", 400)
    


@app_views.route('/users_pictures/<user_id>', methods=['POST'], strict_slashes=False)
def save_user_picture(user_id):
    """save the user picture"""

    if 'image' in request.files:
        image_file = request.files['image']
        file_path = f"/home/ali6500/DEV/Smile-Seeker/api/v1/views/users_pictures/{image_file.filename}.png"
        image_file.save(file_path)
        # update the doctor object
        user = storage.get("Users", user_id)
        if not user:
            abort(404)

        user.update(**{"picture": file_path})
        return {"picturePath": file_path}, 201
    else:
        return {"error": "No image provided"}, 400