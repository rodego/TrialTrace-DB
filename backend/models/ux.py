from backend.main import db
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy import func, text
from sqlalchemy.orm import relationship, backref
from uuid import uuid4
from backend.models.users import *
from backend.models.data import *


class Views(db.Model):
    __tablename__="views"
    view_uid = db.Column(UUID(as_uuid=True),primary_key=True, default=uuid4, nullable=False)
    view_name = db.Column(db.Text)
    view_belongs_to_user = db.Column(UUID(as_uuid=True), db.ForeignKey('users.user_uid'))
    view_has_fields = relationship("Fields", secondary="fieldsviews", backref='view')

    def __repr__(self):
        return f"<View name='{self.view_name}'>"

class FieldsViews (db.Model):
    __tablename__="fieldsviews"
    fieldview_uid = db.Column(UUID(as_uuid=True),primary_key=True, default=uuid4, nullable=False)
    view_uid = db.Column(UUID(as_uuid=True), db.ForeignKey('views.view_uid'))
    field_uid = db.Column(UUID(as_uuid=True), db.ForeignKey('fields.field_uid'))
    field_order = db.Column(db.Integer)
    view = relationship(Views, backref=backref("field_order", cascade="all, delete-orphan"))
    field = relationship(Fields, backref=backref("order_in_view", cascade="all, delete-orphan"))