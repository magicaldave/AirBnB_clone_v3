#!/usr/bin/python3
"""First-level API module"""


from os import getenv
from flask import Flask, jsonify, make_response
from flask_cors import CORS
from models import storage
from api.v1.views import app_view


app = Flask(__name__)
cors = CORS(app, resources={r"/*": {"origins": "0.0.0.0"}})
app.register_blueprint(app_views)


@app.teardown_appcontext
def teardown(junk):
    """
    Closes SQLAlchemy Session.
    """
    storage.close()


@app.errorhandler(404)
def not_found(error):
    """
    Return json-ified 404.
    """
    return make_response(jsonify({"error": "Not found"}), 404)


if __name__ == "__main__":
    h = "0.0.0.0"
    p = "5000"
    if getenv("HBNB_API_HOST"):
        h = getenv('HBNB_API_HOST')
    if getenv("HBNB_API_HOST"):
        p = environ.get('HBNB_API_PORT')

    app.run(host=h, port=p, threaded=True)
