from flask import Flask
from flask_cors import CORS

# Importacion de modulos
from api.test import test

app = Flask(__name__, template_folder='./webpage/build',
            static_url_path='',
            static_folder='./webpage/build')
CORS(app)

# Registramos los modulos
app.register_blueprint(test, url_prefix='/api/test')

if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True)
