#کتاب خانه ها 

from sqlalchemy import *

from extentions import db 

#دیتابیس 


class Product(db.Model):
    __tablename__="products"
    id = Column(Integer , primary_key= True)
    name = Column(VARCHAR)
    price = Column(INTEGER)
    discount = Column(Integer)
    discount_price = Column(INTEGER)
    final_price = Column(Integer)
    descr=Column(VARCHAR)
    stock = Column(Integer)
    active = Column(Integer)
    category_id = Column(Integer , ForeignKey('categories.id'), nullable=True )
    

