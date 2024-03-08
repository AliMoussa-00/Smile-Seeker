"""Index file to get basic info"""
from flask import jsonify, abort, send_file, make_response
import os

from api.v1.views import app_views


@app_views.route('/status', methods=['GET'], strict_slashes=False)
def status():
    """ Status of API """
    return jsonify({"status": "OK"})


@app_views.route('/image/<user_id>', methods=['GET'], strict_slashes=False)
def upload_image(user_id):
    """ upload the user/doc image """
    absolute_path = os.path.dirname(__file__)
    image_path = f"{absolute_path}/users_pictures/user_{user_id}_pic.png"

    if os.path.exists(image_path):
        
        return send_file(image_path, mimetype='image/png')

    else:
        return make_response("Image not found", 400)
