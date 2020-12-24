from authz.model import User

class UserController:

    def get_users():
        return User

    def get_user(user_id):
        return User[int(user_id)]