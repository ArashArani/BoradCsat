from sqlalchemy import *
from sqlalchemy.orm import backref
from extentions import db

class Card(db.Model):
    __tablename__="cards"
    id = Column(Integer , primary_key= True)
    card_owner = Column(VARCHAR)
    card_number = Column(VARCHAR)
    bank_name = Column(VARCHAR)
    status = Column(VARCHAR)

    def status_persian(self):
        if self.status == 'ON':
            return 'فعال'
        elif self.status == 'OFF' :
            return "غیر فعال"