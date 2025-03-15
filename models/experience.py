from sqlalchemy import *

from extentions import db


class Experience(db.Model):
    __tablename__ = 'experiences'
    id = Column(Integer , primary_key=True)
    name = Column(VARCHAR)
    short_desc = Column(VARCHAR)
    long_desc = Column(VARCHAR)
    author = Column(VARCHAR)
    question1 = Column(VARCHAR)
    question2 = Column(VARCHAR)
    awnser1 = Column(VARCHAR)
    awnser2 = Column(VARCHAR)