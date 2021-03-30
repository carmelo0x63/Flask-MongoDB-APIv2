# Flask-MongoDB-APIv2/app.py

from flask import Flask
from flask_bcrypt import Bcrypt
from database.db import initialize_db
from flask_restful import Api
from resources.routes import initialize_routes
from flask_jwt_extended import JWTManager

app = Flask(__name__)
app.config.from_envvar('ENV_FILE_LOCATION')

api = Api(app)
bcrypt = Bcrypt(app)
jwt = JWTManager(app)

app.config['MONGODB_SETTINGS'] = {
    'host': 'mongodb://db/vault-db'
}

initialize_db(app)
initialize_routes(api)

if __name__ == '__main__':
    app.run()

