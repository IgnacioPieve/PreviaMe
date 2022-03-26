import firebase_admin
from firebase_admin import credentials
from flask import Flask
from flask_cors import CORS

# Importacion de modulos
from api.party import party_endpoint
from api.test import test

app = Flask(__name__)
CORS(app)

# Registramos los modulos
app.register_blueprint(party_endpoint, url_prefix='/api/party')
app.register_blueprint(test, url_prefix='/api/test')

# Inicializamos firebase
cred = credentials.Certificate("credentials.json")
firebase_admin.initialize_app(cred)

if __name__ == '__main__':
    app.run()
