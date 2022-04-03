import secure_config

version = 0.1
metadata = {
    "title": 'PreviaMe',
    "version": 0.1,
    "contact": {
        "name": "Ignacio Pieve Roiger",
        "email": "ignacio.pieve@gmail.com",
    },
    "license_info": {
        "name": "Apache 2.0",
        "url": "https://www.apache.org/licenses/LICENSE-2.0.html",
    },
    "description": "¿Qué esperas para organizar tus previas?"
}

db_string = 'mongodb://localhost:27017'
db_name = 'PreviaMe'

firebase_credentials = secure_config.firebase_credentials
