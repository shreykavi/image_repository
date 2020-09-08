import uuid

from app import db
from sqlalchemy.dialects.postgresql import JSON, UUID
from sqlalchemy.orm import relationship
from passlib.apps import custom_app_context as pwd_context
from enum import Enum
from datetime import datetime

class Role(Enum):
    ADMIN = 'admin'
    CUSTOMER = 'customer'

class Permissions(Enum):
    OPEN = 'open'
    PUBLIC_USE = 'public'
    PRIVATE = 'private'

class Result(db.Model):
    __tablename__ = 'test'

    id = db.Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, unique=True, nullable=False)
    url = db.Column(db.String())
    # result_all = db.Column(JSON)
    # result_no_stop_words = db.Column(JSON)

    def __init__(self, url, result_all, result_no_stop_words):
        self.url = url
        # self.result_all = result_all
        # self.result_no_stop_words = result_no_stop_words

    def __repr__(self):
        return '<id {}>'.format(self.id)

class User(db.Model):
    """
    Params:
        email: email address of user
        encrypted password for the user
    """
    __tablename__ = 'users'

    username = db.Column(db.String(32), primary_key=True, unique=True, nullable=False)
    password_hash = db.Column(db.String(128))
    role = db.Column(db.String(32))
    images = relationship("Image")

    def __init__(self, username):
        self.username = username
        self.role = str(Role.CUSTOMER.value) #Default to customer

    def hash_password(self, password):
        self.password_hash = pwd_context.encrypt(password)

    def verify_password(self, password):
        return pwd_context.verify(password, self.password_hash)

class Image(db.Model):
    __tablename__ = 'images'

    filekey = db.Column(UUID(as_uuid=True), primary_key=True, unique=True, nullable=False)
    filename = db.Column(db.String(128))
    ext = db.Column(db.String(128))
    username = db.Column(db.String(32), db.ForeignKey('users.username'))
    timestamp = db.Column(db.DateTime())
    permissions = db.Column(db.String(32))

    def __init__(self, filekey, filename, ext, username, permissions):
        self.filekey = filekey
        self.filename = filename
        self.ext = ext
        self.username = username
        self.timestamp = datetime.utcnow()
        self.permissions = permissions

    # def __repr__(self):
#         return '<id {}>'.format(self.id)