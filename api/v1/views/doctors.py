"""users api endpoints"""
from flask import jsonify, abort

from api.v1.views import app_views
from models import storage


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
