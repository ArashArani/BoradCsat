#کتاب خانه ها 

from sqlalchemy import *

from extentions import db 

#دیتابیس 


class Category(db.Model):
    __tablename__="categories"
    id = Column(Integer , primary_key= True)
    name = Column(VARCHAR)

    
