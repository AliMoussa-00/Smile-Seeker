"""reviews api endpoints"""
import os

from flask import jsonify, abort, request, make_response

from api.v1.views import app_views
from models import storage
from models.reviews import Reviews


@app_views.route('/reviews', methods=['GET'], strict_slashes=False)
def get_reviews():
    """get all reviews"""
    all_reviews = storage.all("Reviews")
    reviews = []
    if all_reviews:
        for review in all_reviews.values():
            reviews.append(review.to_dict())

    return jsonify(reviews)


@app_views.route('/doc_reviews/<doc_id>', methods=['GET'], strict_slashes=False)
def get_doc_reviews(doc_id):
    """get all reviews for a doctor"""

    doc = storage.get("Doctors", doc_id)
    if not doc:
        abort(404, description="Not a Doctor")

    all_reviews = doc.reviews
    reviews = []
    if all_reviews:
        for review in all_reviews:
            reviews.append(review.to_dict())

    return make_response(jsonify(reviews), 200)


@app_views.route('/reviews', methods=['POST'], strict_slashes=False)
def create_review():
    """create a review"""
    if not request.get_json():
        abort(404, description="Not Json")
    
    data = request.get_json()

    if 'comment' not in data:
        abort(404, description="No review comment")
    
    if 'doctor_id' not in data:
        abort(404, description="No doctor Id")
    
    if 'user_id' not in data:
        abort(404, description="No user Id")

    review = Reviews(**data)
    review.save()

    return jsonify(review.to_dict())


@app_views.route('/reviews/<review_id>', methods=['GET'], strict_slashes=False)
def get_review(review_id):
    """get a review instance"""

    review = storage.get("Reviews", review_id)
    if not review:
        abort(404, description="Not a review")

    return jsonify(review.to_dict())


@app_views.route('/reviews/<review_id>', methods=['DELETE'], strict_slashes=False)
def delete_review(review_id):
    """delete a review instance"""

    review = storage.get("Reviews", review_id)
    if not review:
        abort(404, description="Not a Review")

    review.delete()
    storage.save()

    return make_response(jsonify("Review Delete"), 200)