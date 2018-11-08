from . import db
from .mixins import CRUDMixin
from sqlalchemy import Column, TIMESTAMP as Timestamp, String, Integer
from sqlalchemy_utils import force_auto_coercion

force_auto_coercion()


class Call(CRUDMixin, db.Model):
    call_id = Column(Integer)
    start_id = Column(Integer, unique=True)
    end_id = Column(Integer, unique=True)
    source = Column(String(11))
    destination = Column(String(11))
    start_timestamp = Column(Timestamp)
    end_timestamp = Column(Timestamp)
