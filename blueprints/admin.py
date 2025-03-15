from flask import Blueprint, session, request, abort, redirect, render_template, flash, url_for

from random import randint

from flask_mail import Message

import os

from extentions import db, mail

from config import ADMIN_PASSWORD, ADMIN_USERNAME

from models.user import User

from models.consults import Consult

from models.discount import Discount

from models.cart import *

from models.cart_item import CartItem

from models.card import Card

from models.course import Course

from models.course_video import CourseVideo

from extentions import today

from models.blog import Blog

from models.experience import Experience

app = Blueprint('admin', __name__)


@app.before_request
def before_request():
    if (session.get('admin_login', None) is None and
            request.endpoint not in ["admin.main", "admin.pwa"]):
        return abort(403)  # دسترسی ممنوع


@app.route('/pwa')
def pwa():
    try:
        return render_template('pwa.html')
    except:
        return abort(500)


@app.route('/admin/login', methods=["POST", "GET"])
def main():
    if request.method == "GET":

        return render_template("/admin/login.html")
        # سپس بررسی متد POST
    elif request.method == "POST":
        username = request.form.get('username', None)
        password = request.form.get('password', None)

        if username == ADMIN_USERNAME and password == ADMIN_PASSWORD:
            session['admin_login'] = username
            flash('success', "خوش اومدی رئیس !")
            return redirect('/admin/dashboard')
        else:
            flash('error', 'مشکلی پیش آمده ، بعدا تلاش کنید')
            # تولید کد تأییدیه جدید
            return redirect('/admin/login')


@app.route('/admin/dashboard')
def dashboard():
    date = today()

    total_sales = db.session.query(
        func.sum(CartItem.final_price *
                 CartItem.quantity).label('total_revenue')
    ).select_from(CartItem) \
        .join(Cart, CartItem.cart_id == Cart.id) \
        .join(Course, CartItem.course_id == Course.id) \
        .filter(or_(Cart.status == 'In Progress', Cart.status == 'Delivered')) \
        .scalar() or 0
    course_count = Course.query.count()
    user_count = User.query.count()
    consult_count = Consult.query.filter(Consult.status == 'unread').count()
    card_count = Card.query.filter(Card.status == "ON").count()
    cart_count = Cart.query.filter(Cart.status == 'Verify').count()
    return render_template("/admin/dashboard.html", card_count=card_count, cart_count=cart_count, user_count=user_count, consult_count=consult_count, course_count=course_count, date=date, total_sales=total_sales)


@app.route("/admin/dashboard/courses", methods=['POST', "GET"])
def courses():
    date = today()
    card_count = Card.query.filter(Card.status == "ON").count()
    cart_count = Cart.query.filter(Cart.status == 'Verify').count()
    total_sales = db.session.query(
        func.sum(CartItem.final_price *
                 CartItem.quantity).label('total_revenue')
    ).select_from(CartItem) \
        .join(Cart, CartItem.cart_id == Cart.id) \
        .join(Course, CartItem.course_id == Course.id) \
        .filter(or_(Cart.status == 'In Progress', Cart.status == 'Delivered')) \
        .scalar() or 0
    course_count = Course.query.count()
    user_count = User.query.count()
    consult_count = Consult.query.filter(Consult.status == 'unread').count()
    page_list = Course.query.all()
    if request.method == 'GET':
        return render_template("/admin/courses.html", card_count=card_count, cart_count=cart_count, page_list=page_list, user_count=user_count, consult_count=consult_count, course_count=course_count, date=date, total_sales=total_sales)
    else:
        name = request.form.get("name")
        price = int(request.form.get("price"))
        discount = int(request.form.get("discount"))
        short_desc = request.form.get("short_desc")
        long_desc = request.form.get("long_desc")
        teacher = request.form.get("teacher")
        time = request.form.get("time")
        active = request.form.get("active")
        pic = request.files.get("pic")
        if discount == None or '':
            discount = 0

        final_price = price - (price*(discount/100))
        final_price = int(final_price)
        discount_price = int(price * (discount/100))
        c = Course()
        c.name = name
        c.price = price
        c.discount = discount
        c.discount_price = discount_price
        c.final_price = final_price
        c.short_desc = short_desc
        c.long_desc = long_desc
        c.teacher = teacher
        c.time = time
        if active == 'on':
            c.active = 1
        else:
            c.active = 0
        pic.save(f"static/covers/courses/{name}.webp")
        db.session.add(c)
        db.session.commit()
        flash("success", f"دوره ی {name} با موفقیت در سیستم ثبت شد . ")
        return redirect(url_for("admin.courses"))


@app.route("/admin/dashboard/courses/<int:id>", methods=['GET', 'POST'])
def edit_course(id):
    c = Course.query.filter(Course.id == id).first()
    date = today()
    total_sales = db.session.query(
        func.sum(CartItem.final_price *
                 CartItem.quantity).label('total_revenue')
    ).select_from(CartItem) \
        .join(Cart, CartItem.cart_id == Cart.id) \
        .join(Course, CartItem.course_id == Course.id) \
        .filter(or_(Cart.status == 'In Progress', Cart.status == 'Delivered')) \
        .scalar() or 0
    course_count = Course.query.count()
    user_count = User.query.count()
    card_count = Card.query.filter(Card.status == "ON").count()
    cart_count = Cart.query.filter(Cart.status == 'Verify').count()
    consult_count = Consult.query.filter(Consult.status == 'unread').count()
    page_list = CourseVideo.query.filter(CourseVideo.course_id == c.id).all()
    if request.method == 'GET':
        return render_template("/admin/edit-courses.html", c=c, card_count=card_count, cart_count=cart_count, page_list=page_list, user_count=user_count, consult_count=consult_count, course_count=course_count, date=date, total_sales=total_sales)
    else:
        name = request.form.get("name")
        price = int(request.form.get("price"))
        discount = int(request.form.get("discount"))
        short_desc = request.form.get("short_desc")
        long_desc = request.form.get("long_desc")
        teacher = request.form.get("teacher")
        time = request.form.get("time")
        active = request.form.get("active")
        pic = request.files.get("pic")
        if discount == None or '':
            discount = 0

        final_price = price - (price*(discount/100))
        final_price = int(final_price)
        discount_price = int(price * (discount/100))
        c.name = name
        c.price = price
        c.discount = discount
        c.discount_price = discount_price
        c.final_price = final_price
        c.short_desc = short_desc
        c.long_desc = long_desc
        c.teacher = teacher
        c.time = time
        if active == 'on':
            c.active = 1
        else:
            c.active = 0
        if pic.filename != "":
            os.remove(f"static/covers/courses/{c.name}.webp")
            pic.save(f"static/covers/courses/{name}.webp")
        db.session.commit()
        flash("success", f"دوره ی {name} با موفقیت تغییر کرد . ")
        return redirect(url_for("admin.courses"))


@app.route("/delete-course")
def delete_course():
    id = request.args.get("id")
    course = Course.query.filter(Course.id == id).first_or_404()
    db.session.delete(course)
    db.session.commit()
    os.remove(f"sratic/covers/courses/{course.name}.webp")
    flash("success", f"دوره ی {course.name} با موفقیت حذف شد . ")
    return redirect(url_for("admin.courses"))


@app.route("/admin/dashboard/courses/<int:id>/add-video", methods=["POST", "GET"])
def add_video(id):
    course = Course.query.filter(Course.id == id).first_or_404()
    date = today()
    total_sales = db.session.query(
        func.sum(CartItem.final_price *
                 CartItem.quantity).label('total_revenue')
    ).select_from(CartItem) \
        .join(Cart, CartItem.cart_id == Cart.id) \
        .join(Course, CartItem.course_id == Course.id) \
        .filter(or_(Cart.status == 'In Progress', Cart.status == 'Delivered')) \
        .scalar() or 0
    course_count = Course.query.count()
    user_count = User.query.count()
    card_count = Card.query.filter(Card.status == "ON").count()
    cart_count = Cart.query.filter(Cart.status == 'Verify').count()

    consult_count = Consult.query.filter(Consult.status == 'unread').count()
    if request.method == 'GET':
        return render_template("/admin/add-video.html", date=date, card_count=card_count, cart_count=cart_count, total_sales=total_sales, course_count=course_count,
                               user_count=user_count, consult_count=consult_count)
    else:
        name = request.form.get("name")
        link = request.form.get("link")
        short_desc = request.form.get("short_desc")

        v = CourseVideo(name=name, link=link, short_desc=short_desc)
        v.course = course
        db.session.add(v)
        db.session.commit()
        flash("success", f"ویدئو {name} با موفقیت در سیستم ثبت شد . ")
        return redirect(url_for(f"admin.courses", id={course.id}))


@app.route("/delete-video")
def delte_video():
    id = request.args.get("id")
    video = CourseVideo.query.filter(CourseVideo.id == id).first()
    flash("success", f"ویدئو ی {video.name} با موفقیت حذف شد . ")
    db.session.delete(video)
    db.session.commit()
    return redirect(url_for("admin.courses"))


@app.route("/admin/dashboard/experiences", methods=['POST', 'GET'])
def experiences():
    page_list = Experience.query.all()
    date = today()
    total_sales = db.session.query(
        func.sum(CartItem.final_price *
                 CartItem.quantity).label('total_revenue')
    ).select_from(CartItem) \
        .join(Cart, CartItem.cart_id == Cart.id) \
        .join(Course, CartItem.course_id == Course.id) \
        .filter(or_(Cart.status == 'In Progress', Cart.status == 'Delivered')) \
        .scalar() or 0
    course_count = Course.query.count()
    user_count = User.query.count()
    card_count = Card.query.filter(Card.status == "ON").count()
    cart_count = Cart.query.filter(Cart.status == 'Verify').count()

    consult_count = Consult.query.filter(Consult.status == 'unread').count()

    if request.method == 'GET':
        return render_template("/admin/experiences.html",page_list = page_list , date=date, card_count=card_count, cart_count=cart_count, total_sales=total_sales, course_count=course_count,
                               user_count=user_count, consult_count=consult_count)
    else : 
        name = request.form.get("name")
        author = request.form.get("author")
        short_desc = request.form.get("short_desc")
        long_desc = request.form.get("long_desc")
        question1 = request.form.get("question1")
        question2 = request.form.get("question2")
        awnser1 = request.form.get("awnser1")
        awnser2 = request.form.get("awnser2")
        pic1 = request.files.get("pic1")
        pic2 = request.files.get("pic2")

        e = Experience(name = name , author = author , short_desc = short_desc , long_desc = long_desc , question1 = question1
                       , question2 = question2 , awnser1 = awnser1 , awnser2 = awnser2)
        
        pic1.save(f"static/covers/exp/{name}1.webp")
        pic2.save(f"static/covers/exp/{name}2.webp")

        db.session.add(e)
        db.session.commit()
        flash("success",f'تجربه ی {name} با موفقیت در سیستم ثبت شد . ')
        return redirect(url_for("admin.experiences"))
    

@app.route("/admin/dashboard/experiences/<int:id>",methods=['POST','GET'])
def edit_experience(id):
    e = Experience.query.filter(Experience.id == id).first_or_404()
    date = today()
    total_sales = db.session.query(
        func.sum(CartItem.final_price *
                 CartItem.quantity).label('total_revenue')
    ).select_from(CartItem) \
        .join(Cart, CartItem.cart_id == Cart.id) \
        .join(Course, CartItem.course_id == Course.id) \
        .filter(or_(Cart.status == 'In Progress', Cart.status == 'Delivered')) \
        .scalar() or 0
    course_count = Course.query.count()
    user_count = User.query.count()
    card_count = Card.query.filter(Card.status == "ON").count()
    cart_count = Cart.query.filter(Cart.status == 'Verify').count()

    consult_count = Consult.query.filter(Consult.status == 'unread').count()
    if request.method == 'GET':
        
        return render_template("/admin/edit-experiences.html",e = e , date=date, card_count=card_count, cart_count=cart_count, total_sales=total_sales, course_count=course_count,
                               user_count=user_count, consult_count=consult_count)
    else : 
        name = request.form.get("name")
        author = request.form.get("author")
        short_desc = request.form.get("short_desc")
        long_desc = request.form.get("long_desc")
        question1 = request.form.get("question1")
        question2 = request.form.get("question2")
        awnser1 = request.form.get("awnser1")
        awnser2 = request.form.get("awnser2")
        pic1 = request.files.get("pic1")
        pic2 = request.files.get("pic2")
        e.name = name 
        e.author = author
        e.shrt_desc = short_desc
        e.long_desc = long_desc
        e.question1 = question1
        e.question2 = question2
        e.awnser1 = awnser1
        e.awnser2 = awnser2

        if pic1.filename != '':
            os.remove(f"static/covers/exp/{e.name}1.webp")
            pic1.save(f"static/covers/exp/{name}1.webp")
            

        if pic2.filename != '':
            os.remove(f"static/covers/exp/{e.name}2.webp")
            pic2.save(f"static/covers/exp/{name}2.webp")

        flash("success",f"تجربه ی {name} با موفقیت تغییر کرد .")
        db.session.commit()
        return redirect(url_for("admin.experiences"))

@app.route("/delete-exp")
def delete_exp():
    id = request.args.get("id")
    e = Experience.query.filter(Experience.id == id).first()
    os.remove(f"static/covers/exp/{e.name}1.webp")
    os.remove(f"static/covers/exp/{e.name}2.webp")
    db.session.delete(e)
    flash("success",f"تجربه ی {e.name} با موفقیت حذف شد . ")
    db.session.commit()
    return redirect(url_for("admin.experiences"))

@app.route("/admin/dashboard/blogs",methods=['POST',"GET"])
def blogs():
    page_list = Blog.query.all()
    date = today()
    total_sales = db.session.query(
        func.sum(CartItem.final_price *
                 CartItem.quantity).label('total_revenue')
    ).select_from(CartItem) \
        .join(Cart, CartItem.cart_id == Cart.id) \
        .join(Course, CartItem.course_id == Course.id) \
        .filter(or_(Cart.status == 'In Progress', Cart.status == 'Delivered')) \
        .scalar() or 0
    course_count = Course.query.count()
    user_count = User.query.count()
    card_count = Card.query.filter(Card.status == "ON").count()
    cart_count = Cart.query.filter(Cart.status == 'Verify').count()

    consult_count = Consult.query.filter(Consult.status == 'unread').count()

    if request.method == 'GET':
        return render_template("/admin/blogs.html",page_list = page_list , date=date, card_count=card_count, cart_count=cart_count, total_sales=total_sales, course_count=course_count,
                               user_count=user_count, consult_count=consult_count)
    else : 
        name = request.form.get("name")
        author = request.form.get("author")
        short_desc = request.form.get("short_desc")
        long_desc = request.form.get("long_desc")
        question1 = request.form.get("question1")
        question2 = request.form.get("question2")
        awnser1 = request.form.get("awnser1")
        awnser2 = request.form.get("awnser2")
        pic1 = request.files.get("pic1")
        pic2 = request.files.get("pic2")

        e = Blog(name = name , author = author , short_desc = short_desc , long_desc = long_desc , question1 = question1
                       , question2 = question2 , awnser1 = awnser1 , awnser2 = awnser2)
        
        pic1.save(f"static/covers/blogs/{name}1.webp")
        pic2.save(f"static/covers/blogs/{name}2.webp")

        db.session.add(e)
        db.session.commit()
        flash("success",f'بلاگ {name} با موفقیت در سیستم ثبت شد . ')
        return redirect(url_for("admin.blogs"))
    
@app.route("/admin/dashboard/blogs/<int:id>",methods=['POST','GET'])
def edit_blog(id):
    e = Blog.query.filter(Blog.id == id).first_or_404()
    date = today()
    total_sales = db.session.query(
        func.sum(CartItem.final_price *
                 CartItem.quantity).label('total_revenue')
    ).select_from(CartItem) \
        .join(Cart, CartItem.cart_id == Cart.id) \
        .join(Course, CartItem.course_id == Course.id) \
        .filter(or_(Cart.status == 'In Progress', Cart.status == 'Delivered')) \
        .scalar() or 0
    course_count = Course.query.count()
    user_count = User.query.count()
    card_count = Card.query.filter(Card.status == "ON").count()
    cart_count = Cart.query.filter(Cart.status == 'Verify').count()

    consult_count = Consult.query.filter(Consult.status == 'unread').count()
    if request.method == 'GET':
        
        return render_template("/admin/edit-blogs.html",e = e , date=date, card_count=card_count, cart_count=cart_count, total_sales=total_sales, course_count=course_count,
                               user_count=user_count, consult_count=consult_count)
    else : 
        name = request.form.get("name")
        author = request.form.get("author")
        short_desc = request.form.get("short_desc")
        long_desc = request.form.get("long_desc")
        question1 = request.form.get("question1")
        question2 = request.form.get("question2")
        awnser1 = request.form.get("awnser1")
        awnser2 = request.form.get("awnser2")
        pic1 = request.files.get("pic1")
        pic2 = request.files.get("pic2")
        e.name = name 
        e.author = author
        e.shrt_desc = short_desc
        e.long_desc = long_desc
        e.question1 = question1
        e.question2 = question2
        e.awnser1 = awnser1
        e.awnser2 = awnser2

        if pic1.filename != '':
            os.remove(f"static/covers/blogs/{e.name}1.webp")
            pic1.save(f"static/covers/blogs/{name}1.webp")
            

        if pic2.filename != '':
            os.remove(f"static/covers/blogs/{e.name}2.webp")
            pic2.save(f"static/covers/blogs/{name}2.webp")

        flash("success",f"بلاگ {name} با موفقیت تغییر کرد .")
        db.session.commit()
        return redirect(url_for("admin.blogs"))



@app.route("/delete-blog")
def delete_blog():
    id = request.args.get("id")
    e = Blog.query.filter(Blog.id == id).first()
    os.remove(f"static/covers/blogs/{e.name}1.webp")
    os.remove(f"static/covers/blogs/{e.name}2.webp")
    db.session.delete(e)
    flash("success",f"بلاگ {e.name} با موفقیت حذف شد . ")
    db.session.commit()
    return redirect(url_for("admin.blogs"))

@app.route("/admin/dashboard/cards",methods=['POST',"GET"])
def cards():
    page_list = Card.query.all()
    date = today()
    total_sales = db.session.query(
        func.sum(CartItem.final_price *
                 CartItem.quantity).label('total_revenue')
    ).select_from(CartItem) \
        .join(Cart, CartItem.cart_id == Cart.id) \
        .join(Course, CartItem.course_id == Course.id) \
        .filter(or_(Cart.status == 'In Progress', Cart.status == 'Delivered')) \
        .scalar() or 0
    course_count = Course.query.count()
    user_count = User.query.count()
    card_count = Card.query.filter(Card.status == "ON").count()
    cart_count = Cart.query.filter(Cart.status == 'Verify').count()

    consult_count = Consult.query.filter(Consult.status == 'unread').count()

    if request.method == 'GET':
        return render_template("/admin/cards.html",page_list = page_list , date=date, card_count=card_count, cart_count=cart_count, total_sales=total_sales, course_count=course_count,
                               user_count=user_count, consult_count=consult_count)
    else :
        card_owner = request.form.get("card_owner")
        card_number = request.form.get("card_number")
        bank_name = request.form.get("bank_name")
        status = request.form.get("status")
        c = Card()
        c.card_owner = card_owner
        c.bank_name = bank_name
        c.card_number =card_number
        c.status = status
        db.session.add(c)
        db.session.commit()
        flash("success",f'کارت {bank_name} با موفقیت در سیستم ثبت شد . ')
        return redirect(url_for("admin.cards"))


@app.route("/admin/dashboard/cards/<int:id>",methods=['POST',"GET"])
def edit_cards(id):
    c = Card.query.filter(Card.id == id).first()
    date = today()
    total_sales = db.session.query(
        func.sum(CartItem.final_price *
                 CartItem.quantity).label('total_revenue')
    ).select_from(CartItem) \
        .join(Cart, CartItem.cart_id == Cart.id) \
        .join(Course, CartItem.course_id == Course.id) \
        .filter(or_(Cart.status == 'In Progress', Cart.status == 'Delivered')) \
        .scalar() or 0
    course_count = Course.query.count()
    user_count = User.query.count()
    card_count = Card.query.filter(Card.status == "ON").count()
    cart_count = Cart.query.filter(Cart.status == 'Verify').count()

    consult_count = Consult.query.filter(Consult.status == 'unread').count()

    if request.method == 'GET':
        return render_template("/admin/edit-card.html",c =c , date=date, card_count=card_count, cart_count=cart_count, total_sales=total_sales, course_count=course_count,
                               user_count=user_count, consult_count=consult_count)
    else :
        card_owner = request.form.get("card_owner")
        card_number = request.form.get("card_number")
        bank_name = request.form.get("bank_name")
        status = request.form.get("status")
        c.card_owner = card_owner
        c.bank_name = bank_name
        c.card_number =card_number
        c.status = status
        db.session.commit()
        flash("success",f'کارت {bank_name} با موفقیت تغییر کرد . ')
        return redirect(url_for("admin.cards"))

@app.route("/delete-card")
def delete_card():
    id = request.args.get("id")
    c = Card.query.filter(Card.id == id).first()
    flash("success",f'کارت {c.bank_name} با موفقیت حذف شد . ')
    db.session.delete(c)
    db.session.commit()
    return redirect(url_for("admin.cards"))