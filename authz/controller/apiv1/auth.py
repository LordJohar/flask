from flask import request, abort
from authz.model import User
from authz.schema.apiv1 import UserSchema
from authz.config import Config
from jwt.exceptions import ExpiredSignatureError, InvalidTokenError
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
            if user.password == data["password"]:  # check password
                current_time = time()
                jwt_token = encode(
                    {
                        "user_id": user.id,
                        "username": user.username,
                        "iss": "auth1",  # issuer
                        "iat": current_time,  # issued at
                        "nbf": current_time,  # not before
                        "exp": current_time + Config.JWT_TOKEN_LIFETIME  # expiration time
                    },
                    Config.SECRET,
                    algorithm=Config.JWT_ALGO
                )  # .decode("utf8")  # data is binary, so it should be changed to utf-8
                return {"user": user_schema.dump(user)}, 201, {
                    "X-Subject-Token": jwt_token}  # 201=created . this is body + header
            else:  # wrong pass
                abort(401)  # unauthorized
        else:
            abort(400)

    def verify_token():
        if not request.is_json:  # If it is not json >>> no problem
            abort(415)
        if "X-Subject-Token" not in request.headers:
            abort(400)
        # we should read the header and verify it
        jwt_token = request.headers.get("X-Subject-Token")

        try:
            jwt_token_data = decode(
                jwt_token,
                Config.SECRET,
                algorithms=[Config.JWT_ALGO]  # if we should not specify this >>> a security breach ("none algorithm")
                # now we should exception on github page of pyjwt
                # https://github.com/jpadilla/pyjwt/blob/master/jwt/exceptions.py
                # https://pyjwt.readthedocs.io/en/stable/api.html
            )

        except ExpiredSignatureError:
            abort(401, "Token expired")
        except InvalidTokenError:
            abort(400, "Invalid token")
        except:  # other exceptions
            abort(400)
        user = User.query.get(jwt_token_data["user_id"])  # find the user for verification
        if user is None:
            abort(404)  # no user found
        # we can check other user options like: is_enabled, expiration time
        user_schema = UserSchema()
        return {"user": user_schema.dump(user)}, 200, {"X-Subject-Token": jwt_token}  # 200: ok
