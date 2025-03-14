#کتاب خانه ها 

from sqlalchemy import *

from extentions import db 

#دیتابیس 


class Consult(db.Model):
    __tablename__="consults"
    id = Column(Integer , primary_key= True)
    name = Column(VARCHAR)
    subject = Column(VARCHAR)
    text = Column(VARCHAR)
    status = Column(VARCHAR) 

    def persian_status(self):
        if self.status == "unread" :
            return "برسی نشده"
        elif self.status == 'readed' :
            return 'برسی شده'