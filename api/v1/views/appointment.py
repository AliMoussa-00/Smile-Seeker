"""appointments api endpoints"""
import os

from flask import jsonify, abort, request, make_response

from api.v1.views import app_views
from models import storage
from models.appointment import Appointments
from dateutil.parser import isoparse


@app_views.route('/appointments', methods=['GET'], strict_slashes=False)
def get_appoints():
    """get all appointments"""
    all_appoints = storage.all("Appointments")
    appoints = []
    if all_appoints:
        for appoint in all_appoints.values():
            appoint.append(appoint.to_dict())

    return jsonify(appoints)


@app_views.route('/appointments', methods=['POST'], strict_slashes=False)
def create_appoint():
    """create appointments"""
    if not request.get_json():
        abort(404, description="Not Json")
    
    data = request.get_json()

    if 'appointment_date' not in data:
        abort(404, description="No appointment Date")
    
    if 'doctor_id' not in data:
        abort(404, description="No doctor Id")
    
    if 'user_id' not in data:
        abort(404, description="No user Id")

    data['appointment_date'] = isoparse(data['appointment_date'])

    appoint = Appointments(**data)
    appoint.save()

    return {"appointment created": appoint.id}, 201

