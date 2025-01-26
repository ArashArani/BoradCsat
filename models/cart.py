from sqlalchemy import *
from sqlalchemy.orm import backref
from extentions import db

class Cart(db.Model):
    __tablename__="carts"
    id = Column(Integer , primary_key= True)
    status = Column(String, default='pending')
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
    discount = Column(Integer , default=0)
    user = db.relationship('User',backref=backref('carts', lazy ='dynamic'))

    
    def total_price(self):
        total = 0
        for item in self.cart_items:
            total += item.price * item.quantity
            
        return total
    
    def total_discount(self):
        total = 0
        for item in self.cart_items:
            total += (item.discount_price * item.quantity) + self.discount

        return total 
    
    def final_price(self):
        total = 0 
        for item in self.cart_items :
            total += (item.final_price * item.quantity) - self.discount
        
        return total

