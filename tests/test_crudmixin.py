from datetime import datetime
from sqlalchemy import Column, DateTime, Unicode
from app import db as _db
from app.mixins import CRUDMixin


class Doc(CRUDMixin, _db.Model):
    __tablename__ = 'document'
    name = Column(Unicode(50))
    created_at = Column(DateTime)


def test_unico(db):
    assert Doc.get_by_id('x87x') is None

    doc1 = Doc.create(name='proposta')
    doc2 = Doc.create(name='manual')
    assert doc1 is not None
    assert doc2 is not None
    assert doc1 == Doc.query.first()
    assert doc2 == Doc.get_by_id('2')

    agora = datetime.utcnow()
    doc1.created_at = agora
    doc1.save()
    doc2.update(created_at=agora)
    assert agora == Doc.query.get(1).created_at == Doc.query.order_by(Doc.id)\
                                                      .limit(1).offset(1).first().created_at
    doc1.delete()
    assert Doc.query.get(1) is None
