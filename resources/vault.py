# Flask-MongoDB-APIv2/resources/vault.py

from flask import Response, request
from flask_jwt_extended import jwt_required, get_jwt_identity
from database.models import Vault, User
from flask_restful import Resource

class VaultsApi(Resource):
    def get(self):
        vaults = Vault.objects().to_json()
        return Response(vaults, mimetype = "application/json", status = 200)

    @jwt_required()
    def post(self):
        user_id = get_jwt_identity()
        body = request.get_json()
        user = User.objects.get(id = user_id)
        vault = Vault(**body, added_by = user)
        vault.save()
        user.update(push__vault_items = vault)
        user.save()
        id = vault.id
        return {'id': str(id)}, 200
 
class VaultApi(Resource):
    @jwt_required()
    def put(self, id):
        user_id = get_jwt_identity()
        vault = Vault.objects.get(id = id, added_by = user_id)
        body = request.get_json()
        Vault.objects.get(id = id).update(**body)
        return '', 200
 
    @jwt_required()
    def delete(self, id):
        user_id = get_jwt_identity()
        vault = Vault.objects.get(id = id, added_by = user_id)
        vault.delete()
        return '', 200

    def get(self, id):
        vaults = Vault.objects.get(id = id).to_json()
        return Response(vaults, mimetype = "application/json", status = 200)

