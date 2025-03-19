from flask import Blueprint , session , request , abort , redirect , render_template , flash , url_for , jsonify

from flask_login import current_user

import os


from config import ADMIN_PASSWORD , ADMIN_USERNAME

from models.user import User

from models.cart import *

from models.consults import Consult

from models.cart_item import CartItem

from models.experience import Experience

from models.course_video import CourseVideo

from models.card import Card

from models.course import *

from models.blog import Blog

app = Blueprint('general',__name__)

@app.route("/")
def main():
    course_list = Course.query.all()
    exp_list = Experience.query.order_by(func.random()).limit(2).all()
    blog_list = Blog.query.order_by(func.random()).limit(2).all()
    return render_template("home.html", exp_list = exp_list ,course_list = course_list , blog_list = blog_list)

@app.route("/courses/<name>")
def course(name):
    c = Course.query.filter(Course.name == name).first_or_404()
    video_list = CourseVideo.query.filter(CourseVideo.course == c).all()
    other_course = Course.query.filter(Course.name != name).order_by(func.random()).limit(1).all()

    if current_user.is_authenticated:
        purchased_items = current_user.carts.filter(Cart.status == 'Approved').join(
            CartItem).filter(CartItem.course == c).all()
        return render_template("course-info.html",c=c ,other_course = other_course ,video_list = video_list , purchased_items = purchased_items)
    else :
        return render_template("course-info.html",c=c ,other_course = other_course ,video_list = video_list)
    

@app.route("/consults",methods=['POST','GET'])
def consult():
    if request.method == 'GET' :
        return render_template("consults.html")
    else : 
        f_name = request.form.get("f_name")
        l_name = request.form.get("l_name")
        phone = request.form.get("phone")
        subject = request.form.get("subject")
        text = request.form.get("text")

        consult = Consult.query.filter(Consult.phone == phone).filter(Consult.status == 'unread').first()
        if consult is None :
            c = Consult()
            c.f_name = f_name
            c.l_name = l_name
            c.phone = phone
            c.status = 'unread'
            c.subject = subject
            c.text = text
            db.session.add(c)
            db.session.commit()
            flash("success",f'{f_name} عزیر ، درخواست مشاوره شما با موفقیت ثبت شد . ')
            return redirect("/")
        else :
            flash("error",f'{f_name} عزیز ، شما درخواست برسی نشده دارید . ')
            return redirect("/")