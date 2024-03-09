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


@app_views.route('/doc_appointments/<doc_id>', methods=['GET'], strict_slashes=False)
def get_doc_appoints(doc_id):
    """get all appointments for a doctor"""

    doc = storage.get("Doctors", doc_id)
    if not doc:
        abort(404, description="Not a Doctor")

    print(doc.appointments)
    all_appoints = doc.appointments
    appoints = []
    if all_appoints:
        for appoint in all_appoints:
            appoints.append(appoint.to_dict())

    return make_response(jsonify(appoints), 200)


@app_views.route('/appointments/<apppoint_id>', methods=['DELETE'], strict_slashes=False)
def delete_appointment(apppoint_id):
    """delete an appointment instance"""

    appoint = storage.get("Appointments", apppoint_id)
    if not appoint:
        abort(404, description="Not an Appointment")

    appoint.delete()
    storage.save()

    return make_response(jsonify("Appointment Delete"), 200)


@app_views.route('/appointments/<apppoint_id>', methods=['PUT'], strict_slashes=False)
def update_appointment(apppoint_id):
    """update an appointment instance"""

    appoint = storage.get("Appointments", apppoint_id)
    if not appoint:
        abort(404, description="Not an Appointment")

    if not request.get_json():
        abort(404, description="Not Json")

    data = request.get_json()
    if 'appointment_date' not in data:
        abort(404, description="No appointment Date")
    
    appoint.update(**data)

    return make_response(jsonify("Appointment Updated"), 200)