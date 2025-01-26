from sqlalchemy import *
from sqlalchemy.orm import backref
from extentions import db

class Card(db.Model):
    __tablename__="cards"
    id = Column(Integer , primary_key= True)
    account_name = Column(VARCHAR)
    sort_code=Column(VARCHAR)
    account_number=Column(VARCHAR)
    status = Column(VARCHAR)