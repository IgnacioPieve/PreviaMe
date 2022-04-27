import os

import hjson

title = "PreviaMe"
version = 0.1
metadata = {
    "title": title,
    "version": version,
    "contact": {
        "name": f"{title} Team",
        "email": "test@gmail.com",  # TODO: Poner un email
    },
    "license_info": {
        "name": "Apache 2.0",
        "url": "https://www.apache.org/licenses/LICENSE-2.0.html",
    },
    "description": "¿Qué esperas para organizar tus previas?",  # Aca se puede poner markdown
}

db_string = os.getenv("PREVIAME_DB_STRING")
db_name = "PreviaMe"

firebase_json = dict(hjson.loads(os.getenv("PREVIAME_FIREBASE_JSON")))
firebase_private_key = os.getenv("PREVIAME_FIREBASE_PRIVATE_KEY").replace("\\n", "\n")
firebase = {**firebase_json, "private_key": firebase_private_key}
firebase_key = os.getenv("PREVIAME_FIREBASE_KEY")
