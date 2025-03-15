#کتاب خانه ها 

from sqlalchemy import *

from extentions import db 

#دیتابیس 


class Blog(db.Model):
    __tablename__="blogs"
    id = Column(Integer , primary_key= True)
    name = Column(VARCHAR)
    author = Column(VARCHAR)
    short_desc=Column(VARCHAR)
    long_desc=Column(VARCHAR)
    question1 = Column(VARCHAR)
    question2 = Column(VARCHAR)
    awnser1 = Column(VARCHAR)
    awnser2 = Column(VARCHAR)

