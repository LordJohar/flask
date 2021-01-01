from functools import wraps
from flask import abort, request
from jwt import decode
from jwt.exceptions import ExpiredSignatureError, InvalidTokenError
from authz.config import Config

from authz.model import User


def auth_required(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        if not request.is_json:
            abort(415, "Request is not JSON")
        if "X-Auth-Token" not in request.headers:
            abort(400, "Token is not in header")
        jwt_token = request.headers.get("X-Auth-Token")
        try:
            jwt_token_data = decode(
                jwt_token,
                Config.SECRET,
                algorithms=[Config.JWT_ALGO]
            )
        except ExpiredSignatureError:
            abort(401, "Token expired")
        except InvalidTokenError:
            abort(400, "Invalid token")
        except:  # other exceptions
            abort(400)
        user = User.query.get(jwt_token_data["user_id"])
        if user is None:
            abort(404, "User not found")
        return func(*args, **kwargs)


    return wrapper

