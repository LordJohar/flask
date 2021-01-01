from flask import request, abort
from authz.model import User
from authz.schema.apiv1 import UserSchema
from authz.config import Config

from jwt import encode, decode
from time import time


class AuthController:

    def create_token():
        if not request.is_json:
            abort(415)
        user_schema = UserSchema()  # read schema
        data = user_schema.load(request.get_json())
        if "username" in data and "password" in data:
            user = User.query.filter_by(username=data[
                "username"]).first()  # check if username exists. This the the data that the user has entered
            if user is None:
                abort(404)
            if user.password == data["password"]:
                current_time = time()
                # print ("###########-1")
                jwt_token = encode(
                    {
                        "user_id": user.id,
                        "username": user.username,
                        "iss": "auth1",  # issuer
                        "iat": current_time,  # when issued
                        "nbf": current_time,  # not before
                        "exp": current_time + Config.JWT_TOKEN_LIFETIME  # expiration

                    },
                    Config.SECRET,
                    algorithm=Config.JWT_ALGO
                )  # .decode("utf8")  # data is binary, so it should be changed to utf-8
                # print ("###########-2")
                return {"user": user_schema.dump(user)}, 201, {
                    "X-Subject-Token": jwt_token}  # 201=created . this is body + header


            else:  # wrong pass

                abort(401)  # unauthorized



        else:
            abort(400)


def verify_token():
        pass
