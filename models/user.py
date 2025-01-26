#کتاب خانه ها 

from sqlalchemy import *
from extentions import db
from flask_login import UserMixin

#دیتابیس 


class User(db.Model, UserMixin):
    __tablename__="users"
    id = Column(Integer , primary_key= True)
    email = Column(VARCHAR)
    phone = Column(VARCHAR)
    f_name = Column(VARCHAR , nullable=True , default='None')
    l_name = Column(VARCHAR , nullable=True , default='None')
    password = Column(VARCHAR)

    

    