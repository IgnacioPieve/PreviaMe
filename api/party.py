from firebase_admin import auth
from flask import Blueprint, request
from database import db
import api.utils as utils
import uuid

party_endpoint = Blueprint('party', __name__)
collection = db['party']


@party_endpoint.route('/', methods=['POST', 'GET'])
def party_endpoint_function():
    # ----- BEGIN AUTHENTICATION -----
    if request.method == 'POST':
        try:
            token = request.headers.get('Authorization', None).replace('Bearer ', '')
            user_data = auth.verify_id_token(token)
        except Exception as exception:
            return {"error": "Error authenticating", 'exception': str(exception)}, 401
    # -----  END AUTHENTICATION -----

    if request.method == 'POST':
        required_fields = ['geopoint']
        assert_status, fields = utils.assert_fields(request.json, required_fields)
        if assert_status is False:
            return fields, 400

        body = {
            **fields,
            'id': str(uuid.uuid4()),
        }

        collection.insert_one(body)

    return body, 200
