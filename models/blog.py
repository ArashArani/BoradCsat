#کتاب خانه ها 

from sqlalchemy import *

from extentions import db 

#دیتابیس 


class Blog(db.Model):
    __tablename__="blogs"
    id = Column(Integer , primary_key= True)
    name = Column(VARCHAR)
    price = Column(INTEGER)
    short_desc=Column(VARCHAR)
    long_desc=Column(VARCHAR)
    active = Column(Integer)
    category_id = Column(Integer , ForeignKey('categories.id'), nullable=True )
    

