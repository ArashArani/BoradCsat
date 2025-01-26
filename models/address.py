#کتاب خانه ها 

from sqlalchemy import *

from extentions import db 

#دیتابیس 


class Address(db.Model):
    __tablename__="addresses"
    id = Column(Integer , primary_key= True)
    address = Column(VARCHAR)
    name = Column(VARCHAR)
    city = Column(VARCHAR)
    neighborhood = Column(VARCHAR)
    post_code = Column(VARCHAR)
    plaque = Column(INTEGER)
    reciver_f_name = Column(VARCHAR)
    reciver_l_name = Column(VARCHAR)
    phone = Column(VARCHAR)
    user_id = Column(Integer,ForeignKey('users.id'),nullable=False)
    

