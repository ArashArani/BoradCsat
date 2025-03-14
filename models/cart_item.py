from sqlalchemy import *
from sqlalchemy.orm import backref
from extentions import db

class CartItem(db.Model):
    __tablename__="cart_items"
    id = Column(Integer , primary_key= True)
    price = Column(Integer)
    final_price = Column(Integer)
    discount_price = Column(Integer)
    quantity = Column(Integer)
    course_id = Column(Integer , ForeignKey('courses.id'), nullable=False)
    cart_id = Column(Integer , ForeignKey('carts.id'), nullable=False)
    course = db.relationship('Course',backref='cart_items')
    cart = db.relationship('Cart',backref=backref('cart_items' , lazy='dynamic'))