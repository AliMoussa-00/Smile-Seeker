"""Flask application"""
from os import environ

from flask import Flask, make_response, jsonify

from api.v1.views import app_views
from models import storage

app = Flask(__name__)
app.register_blueprint(app_views)


@app.teardown_appcontext
def close_db(error):
    """ Close Storage """
    storage.close()


@app.errorhandler(404)
def not_found(error):
    """ 404 Error"""
    return make_response(jsonify({'error': "Not found"}), 404)


if __name__ == "__main__":
    host = environ.get('SS_API_HOST')
    port = environ.get('SS_API_PORT')
    if not host:
        host = '0.0.0.0'
    if not port:
        port = '5000'
    app.run(host=host, port=int(port), threaded=True)
