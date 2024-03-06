"""users api endpoints"""
import os
import hashlib

from flask import jsonify, abort, request, make_response

from api.v1.views import app_views
from models import storage
from models.doctors import Doctors
from models.location import Location


@app_views.route('/doctors', methods=['GET'], strict_slashes=False)
def get_doctors():
    """get all doctors"""
    all_docs = storage.all("Doctors")
    docs = []
    if all_docs:
        for doc in all_docs.values():
            docs.append(doc.to_dict())

    return jsonify(docs)


@app_views.route('/doctors/<doc_id>', methods=['GET'], strict_slashes=False)
def get_doc(doc_id):
    """get a doctor"""
    doc = storage.get("Doctors", doc_id)
    if not doc:
        abort(404)
    return jsonify(doc.to_dict())


@app_views.route('/doctors', methods=['POST'], strict_slashes=False)
def create_doc():
    """create a doctor object"""
    if not request.get_json():
        abort(404, description="Not Json")
    data = request.get_json()
    address = None
    if 'address' in data:
        address = data['address']
        del data['address']

    doc = Doctors(**data)
    doc.save()
    # save location
    if address:
        loc_dict = {"doctor_id": doc.id, "address": address}
        location = Location(**loc_dict)
        location.save()
    return make_response(jsonify(doc.id), 201)


@app_views.route('/doctors_pictures/<doc_id>', methods=['POST'], strict_slashes=False)
def get_doc_picture(doc_id):
    """get the doctor picture"""

    if 'image' in request.files:
        image_file = request.files['image']
        file_path = f"/home/ali6500/DEV/Smile-Seeker/users_pictures/{image_file.filename}.png"
        image_file.save(file_path)
        # update the doctor object
        doc = storage.get("Doctors", doc_id)
        if not doc:
            abort(404)

        doc.update(**{"picture": file_path})
        return {"picturePath": file_path}, 201
    else:
        return {"error": "No image provided"}, 400


@app_views.route('/log_doc', methods=['POST'], strict_slashes=False)
def loginDoc():
    """check if user exists to login"""
    if not request.get_json():
        abort(404, description="Not Json")
    data = request.get_json()

    if "email" not in data or "password" not in data:
        abort(404, description="email or password is missing")
    
    hashed_password = hashlib.md5(data['password'].encode('utf-8')).hexdigest()

    doc = storage.login(Doctors, data['email'], hashed_password)
    if doc:
        return make_response(jsonify(doc.to_dict()), 201)
    else:
        return make_response("not registered", 400)


