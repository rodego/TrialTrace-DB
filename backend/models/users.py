from backend.main import db
from flask_login import UserMixin
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy import func, text
from uuid import uuid4



class UUserMixin(UserMixin):
    def get_id(self):
        try:
            return self.user_uid
        except AttributeError:
            raise NotImplementedError('No `user_uid` attribute - override `get_id`')

class Users(db.Model, UUserMixin):
    __tablename__ = 'users'
    user_uid = db.Column(UUID(as_uuid=True),
                          primary_key=True, default=uuid4, nullable=False)
    email = db.Column(db.String, nullable=False, unique=True)
    password = db.Column(db.String, nullable=False)
    is_admin = db.Column(db.Boolean, default=False)
    
    def __init__(self, email, password, is_admin):
        self.email = email
        self.password = password
        self.is_admin = is_admin

class Whitelist(db.Model):
    __tablename__ = 'whitelist'
    domain_uid = db.Column(UUID(as_uuid=True),
                          primary_key=True, default=uuid4, nullable=False)
    domain = db.Column(db.String, nullable=False, unique=True)
    
    def __init__(self, domain):
        self.domain = domain