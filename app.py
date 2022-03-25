from flask import Flask
from flask_cors import CORS

# Importacion de modulos
from api.test import test

app = Flask(__name__)
CORS(app)

# Registramos los modulos
app.register_blueprint(test, url_prefix='/api/test')

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080)
