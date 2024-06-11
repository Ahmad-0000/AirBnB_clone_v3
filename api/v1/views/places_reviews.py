#!/usr/bin/python3
"""Reviews blueprint"""
from flask import jsonify, abort, request, make_response
from api.v1.views import app_views


@app_views.route("/places/<uuid:place_id>/reviews", strict_slashes=False)
def place_reviews(place_id):
    """Retrieve one place reviews from storage"""
    from models import storage
    from models.place import Place

    place = storage.get(Place, str(place_id))
    if not place:
        abort(404)
    reviews = place.reviews
    return make_response(jsonify([review.to_dict() for review in reviews]),
                         200)


@app_views.route("/reviews/<uuid:review_id>", strict_slashes=False)
def one_review(review_id):
    """Retrieve one review from storage"""
    from models import storage
    from models.review import Review

    review = storage.get(Review, str(review_id))
    if not review:
        abort(404)
    return make_response(jsonify(review.to_dict()), 200)


@app_views.route("/reviews/<uuid:review_id>", strict_slashes=False,
                 methods=['DELETE'])
def delete_review(review_id):
    """Delete one review from storage"""
    from models import storage
    from models.review import Review

    review = storage.get(Review, str(review_id))
    if not review:
        abort(404)
    storage.delete(review)
    storage.save()
    return make_response(jsonify({}), 200)


@app_views.route("/places/<uuid:place_id>/reviews", strict_slashes=False,
                 methods=['POST'])
def new_review(place_id):
    """Create new review"""
    from models import storage
    from models.place import Place
    from models.review import Review
    from models.user import User

    place = storage.get(Place, str(place_id))
    if not place:
        abort(404)
    if not request.is_json:
        abort(400, "Not a JSON")
    request_data = request.get_json()
    if "user_id" not in request_data:
        abort(400, "Missing user_id")
    user = storage.get(User, request_data['user_id'])
    if not user:
        abort(404)
    if "text" not in request_data:
        abort(400, "Missing text")
    new_review = Review(**request_data)
    new_review.save()
    return make_response(jsonify(new_review.to_dict()), 201)


@app_views.route("/reviews/<uuid:review_id>", strict_slashes=False,
                 methods=['PUT'])
def update_review(review_id):
    """Update review info"""
    from models import storage
    from models.review import Review

    review = storage.get(Review, str(review_id))
    if not review:
        abort(404)
    if not request.is_json:
        abort(400, "Not a JSON")
    request_data = request.get_json()
    for k, v in request_data.items():
        if k == "id" or k == "user_id" or k == "place_id"\
                    or k == "created_at" or k == "updated_at":
            continue
        review.__dict__[k] = v
    review.save()
    return make_response(jsonify(review.to_dict()), 200)
