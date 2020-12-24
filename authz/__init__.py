from flask import Flask, Blueprint
from flask_restx import Api
from flask_sqlalchemy import SQLAchemy

db = SQLAchemy()

from authz.config import Config #Import application config

apiv1_bp = Blueprint("apiv1", __name__, url_prefix="/api/v1") #Create /api/v1 endpoint.
apiv1 = Api(apiv1_bp)   #Create API for /api/v1 endpoint.

from authz import resource

def create_app():
    app = Flask(__name__)   #Create application instance
    app.config.from_object(Config)  #Set app config.
    db.init_app(app)
    app.register_blueprint(apiv1_bp)    #Register /api/v1 to application.
    return app  #Return app instance to caller.

