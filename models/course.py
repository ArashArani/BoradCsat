#کتاب خانه ها 

from sqlalchemy import *

from extentions import db 

#دیتابیس 


class Course(db.Model):
    __tablename__="courses"
    id = Column(Integer , primary_key= True)
    name = Column(VARCHAR)
    price = Column(INTEGER)
    discount = Column(Integer)
    discount_price = Column(INTEGER)
    final_price = Column(INTEGER)
    short_desc=Column(VARCHAR)
    long_desc=Column(VARCHAR)
    teacher = Column(VARCHAR)
    time = Column(VARCHAR)
    active = Column(INTEGER)
    def active_show(self):
        if self.active == 1:
            return 'فعال'
        else :
            return 'غیر فعال'