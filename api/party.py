from flask import Blueprint, request
from database import db

party_endpoint = Blueprint('party', __name__)
collection = db['party']


@party_endpoint.route('/')
def party_endpoint_function():
    if request.method == 'POST':
        collection.insert_one({'test'})

    return {'status': 'ok'}, 200
