# Flask-MongoDB-APIv2/resources/routes.py

from .vault import VaultsApi, VaultApi
from .auth import SignupApi, LoginApi

def initialize_routes(api):
    api.add_resource(VaultsApi, '/api/vaults')
    api.add_resource(VaultApi, '/api/vaults/<id>')

    api.add_resource(SignupApi, '/api/auth/signup')
    api.add_resource(LoginApi, '/api/auth/login')

