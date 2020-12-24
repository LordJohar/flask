from authz import db
from shared import uuidgen


class User(db.Model):

    id=db.Column(db.String(64), primary_key=True, default=uuidgen)
    username=db.Column(db.String(128), unique=True, index=True, nullable=False)
    password=db.Column(db.String(256), nullable=False)
