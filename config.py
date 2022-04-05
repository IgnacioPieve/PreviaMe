import secure_config

title = 'PreviaMe'
version = 0.1
metadata = {
    "title": title,
    "version": version,
    "contact": {
        "name": f"{title} Team",
        "email": "test@gmail.com",                                  # TODO: Poner un email
    },
    "license_info": {
        "name": "Apache 2.0",
        "url": "https://www.apache.org/licenses/LICENSE-2.0.html",
    },
    "description": "¿Qué esperas para organizar tus previas?"       # Aca se puede poner markdown
}

db_string = 'mongodb://localhost:27017'
db_name = 'PreviaMe'

firebase_credentials = secure_config.firebase_credentials
