#!/usr/bin/python3
"""Main API app"""
from api.v1.views import app_views
from flask import Flask, jsonify, make_response
from models import storage
from os import getenv
from flask_cors import CORS


app = Flask(__name__)
app.register_blueprint(app_views, url_prefix="/api/v1")
CORS(app, resources={'*': {'origins': '0.0.0.0'}})


@app.teardown_appcontext
def refresh(exception):
    """Refressing the objects in the storage"""
    storage.close()


@app.errorhandler(404)
def not_found(error):
    """Custom not found error"""
    not_found = {"error": "Not found"}
    return make_response(jsonify(not_found), 404)


@app.errorhandler(400)
def bad_request(error):
    """Custom bad request error"""
    bad_request = {"message": error.description}
    return make_response(jsonify(bad_request), 400)


if __name__ == "__main__":
    host = getenv("HBNB_API_HOST")
    port = getenv("HBNB_API_PORT")
    if host:
        if port:
            app.run(host=host, port=port, threaded=True)
        else:
            app.run(host=host, port=5000, threaded=True)
    elif port:
        if host:
            app.run(host=host, port=port, threaded=True)
        else:
            app.run(host="0.0.0.0", port=port, threaded=True)
    else:
        app.run(host="0.0.0.0", port=5000, threaded=True)
