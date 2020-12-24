from flask_restx import Resource

from authz.controller.apiv1 import UserController

class UserResource(Resource):

    def get(self, user_id=None):
        """
        GET /users --> Get users collection.
        GET /users/<user_id> --> Get single user.
        """
        if user_id is None:
            return UserController.get_users()   #Get users collection.
        else:
            return UserController.get_user(user_id)     #Get single user.

    def post(self):
        pass

    def patch(self):
        pass

    def delete(self):
        pass

