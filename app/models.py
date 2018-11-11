from . import db
from .mixins import CRUDMixin
from sqlalchemy import Column, TIMESTAMP as Timestamp, String, Numeric  # noqa: N811
from sqlalchemy_utils import force_auto_coercion

force_auto_coercion()


class Call(CRUDMixin, db.Model):
    source = Column(String(11))
    destination = Column(String(11))
    start_timestamp = Column(Timestamp)
    end_timestamp = Column(Timestamp)
    price = Column(Numeric(10, 2))
