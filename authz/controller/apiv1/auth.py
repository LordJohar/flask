from flask import request, abort
from authz.model import User
from authz.schema.apiv1 import UserSchema
from authz.config import Config

from jwt import encode, decode
from time import time

class AuthController:

    def create_token():
        user_schema = UserSchema()
        data = user_schema.load(request.get.json())
        if "username" in data and "password" in data:
            user = User.query.filterby(username=["username"]).first
            if user is None:
                abort(404)
            if user.password == data["password"]:
                current_time = time()
                jwt_token = encode(
                    {
                        "username": user.username,
                        "iss": "authz",
                        "iat": current_time,
                        "nbf": current_time,
                        "exp": current_time + Config.JWT_TOKEN_LIFETIME,
                    },
                    Config.SECRET,
                    algorithm=Config.JWT_ALGORITHM
                )
                return { "user": user_schema.dump(user) }, 201, { "X-Subject-Token": jwt_token.decode("utf8") }
            else:
                abort(401)
        else:
            abort(400)

    def verify_token():
        pass