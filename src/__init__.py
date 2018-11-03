# coding=utf-8
from flask import Flask, jsonify
# Import a module / component using its blueprint handler variable (mod_auth)
from .summarizer import document_summarizer


app = Flask(__name__)
# Configurations
app.config.from_object('config')


@app.errorhandler(404)
def not_found(error):
    response = {
        "message": "Error Message: {0}".format(error),
        "status": False
    }

    return jsonify(response)


# Register blueprint(s)
app.register_blueprint(document_summarizer)
