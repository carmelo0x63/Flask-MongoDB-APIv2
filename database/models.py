# Flask-MongoDB-APIv2/database/models.py

from .db import db
from flask_bcrypt import generate_password_hash, check_password_hash

class Vault(db.Document):
    username = db.StringField(required=True, unique = True)
    full_url = db.URLField(required = True)
    short_name = db.StringField(required = True)
    notes = db.ListField(db.StringField())
    added_by = db.ReferenceField('User')

class User(db.Document):
    userid = db.StringField(required = True, unique = True)
    password = db.StringField(required = True, min_length = 6)
    vault_items = db.ListField(db.ReferenceField('Vault', reverse_delete_rule = db.PULL))

    def hash_password(self):
        self.password = generate_password_hash(self.password).decode('utf8')
 
    def check_password(self, password):
        return check_password_hash(self.password, password)

User.register_delete_rule(Vault, 'added_by', db.CASCADE)

