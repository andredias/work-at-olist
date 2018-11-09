from . import db
from .mixins import CRUDMixin
from sqlalchemy import Column, TIMESTAMP as Timestamp, String, Integer  # noqa: N811
from sqlalchemy_utils import force_auto_coercion

force_auto_coercion()


class Call(CRUDMixin, db.Model):
    type = Column(String(5), nullable=False)
    call_id = Column(Integer, nullable=False)
    source = Column(String(11))
    destination = Column(String(11))
    timestamp = Column(Timestamp, nullable=False)
