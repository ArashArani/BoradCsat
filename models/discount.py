from sqlalchemy import *

from extentions import db


class Discount(db.Model):
    __tablename__ = 'discounts'
    id = Column(Integer , primary_key=True)
    amount = Column(INTEGER)
    code = Column(VARCHAR)
    status = Column(VARCHAR)
    user_id = Column(INTEGER , ForeignKey('users.id'))