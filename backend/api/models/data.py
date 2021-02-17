from api import db
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy import func, text
from uuid import uuid4
from api.models.users import *

class Data(db.Model):
    __tablename__ = "data"
    datum_uid = db.Column(UUID(as_uuid=True),
                          primary_key=True, default=uuid4, nullable=False)
    datum_name = db.Column(db.Text)
    datum_value = db.Column(db.Text)
    datum_note = db.Column(db.Text)
    datum_source = db.Column(db.Text)
    created_at = db.Column(db.DateTime, server_default=func.now())
    created_by = db.Column(UUID(as_uuid=True),db.ForeignKey('users.user_uid'))
    datum_depends_on = db.Column(UUID(as_uuid=True), db.ForeignKey('data.datum_uid'))

