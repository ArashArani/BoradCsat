#کتاب خانه ها 

from sqlalchemy import *
from extentions import db
from flask_login import UserMixin

#دیتابیس 


class User(db.Model, UserMixin):
    __tablename__="users"
    id = Column(Integer , primary_key= True)
    username = Column(VARCHAR)
    password = Column(VARCHAR)
    phone = Column(VARCHAR)

    

    