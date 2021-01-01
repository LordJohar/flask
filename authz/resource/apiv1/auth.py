from flask_restx import Resource
from authz.controller.apiv1 import AuthController


class AuthResource(Resource):

    def post(self):
        """
        POST /auth/tokens --> Create new JWT token
        """
        return AuthController.create_token()

    def get():
        """
        GET /auth/tokens --> Verify JWT token

        """
        pass