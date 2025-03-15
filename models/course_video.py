#کتاب خانه ها 

from sqlalchemy import *

from extentions import db 

#دیتابیس 


class CourseVideo(db.Model):
    __tablename__="course_videos"
    id = Column(Integer , primary_key= True)
    name = Column(VARCHAR)
    short_desc=Column(VARCHAR)
    course = db.relationship("Course",backref="course_videos")
    course_id = Column(INTEGER , ForeignKey("courses.id"))    

