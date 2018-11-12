from . import db
from .mixins import CRUDMixin
from datetime import timedelta
from sqlalchemy import Column, TIMESTAMP as Timestamp, String, Numeric, Index  # noqa: N811
from sqlalchemy.event import listens_for
from sqlalchemy_utils import force_auto_coercion

force_auto_coercion()


def calc_price(start_timestamp, end_timestamp):
    '''
    The call price depends on fixed charges,
    call duration and the time of the day that the call was made.
    There are two tariff times:

    Standard time call - between 6h00 and 22h00 (excluding):
        Standing charge: R$ 0,36 (fixed charges that are used to pay
        for the cost of the connection);
        Call charge/minute: R$ 0,09 (there is no fractioned charge.
        The charge applies to each completed 60 seconds cycle).

    Reduced tariff time call - between 22h00 and 6h00 (excluding):
        Standing charge: R$ 0,36
        Call charge/minute: R$ 0,00 (hooray!)

    Examples
    --------

    For a call started at 21:57:13 and finished at 22:17:53 we have:

        Standing charge: R$ 0,36

        Call charge:
            minutes between 21:57:13 and 22:00 = 2
            price: 2 * R$ 0,09 = R$ 0,18

        Total: R$ 0,18 + R$ 0,36 = R$ 0,54
    '''

    if not (start_timestamp and end_timestamp):
        return None
    delta = end_timestamp - start_timestamp
    ref_timestamp = start_timestamp
    price = 0.36
    while delta.seconds > 0:
        std_time = (6, 0) <= (ref_timestamp.hour, ref_timestamp.minute) < (22, 0)
        if std_time:
            t2 = timedelta(hours=22)
        else:
            t2 = timedelta(hours=(6 if ref_timestamp.hour < 6 else 30))
        t1 = timedelta(hours=ref_timestamp.hour, minutes=ref_timestamp.minute,
                       seconds=ref_timestamp.second)
        interval = min(t2 - t1, delta)
        partial_price = (interval.seconds // 60) * 0.09 if std_time else 0
        price += partial_price
        delta -= interval
        ref_timestamp += interval
    return price


class Call(CRUDMixin, db.Model):
    source = Column(String(11))
    destination = Column(String(11))
    start_timestamp = Column(Timestamp)
    end_timestamp = Column(Timestamp)
    price = Column(Numeric(10, 2))


Index('call_idx1', Call.source, Call.end_timestamp)


@listens_for(Call, 'before_insert')
@listens_for(Call, 'before_update')
def listener_calc_price(mapper, connect, target):
    target.price = calc_price(target.start_timestamp, target.end_timestamp)
    return
