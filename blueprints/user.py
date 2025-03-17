from flask import Blueprint , abort , redirect , render_template , flash , request

from flask_login import login_required , login_user , logout_user , current_user

from passlib.hash import sha256_crypt

from models.user import User

from models.cart import Cart

from models.cart_item import CartItem

from models.discount import Discount 

from models.course import Course

from models.course_video import CourseVideo

from extentions import db , today

app = Blueprint("user",__name__)



@app.route("/user/sign-up",methods=['POST',"GET"])
def sign_up():
    if current_user.is_authenticated :
        return redirect("/user/dashboard")
    else:

        if request.method == 'GET':
            return render_template("/user/sign-up.html")
        else :
            username = request.form.get("username")
            password = request.form.get("password")

            user = User.query.filter(User.username == username).first()

            if user == None :
                u = User()
                u.username = username
                u.password = sha256_crypt.hash(password) 
                u.phone = password
                db.session.add(u)
                flash("success",f"اکانت شما با موفقیت ساخته شد . ")
                db.session.commit()
                login_user(u)

                return redirect("/user/dashboard")
            else :
                flash("error",f'نام کاربری {username} در سیستم ثبت شده . ')
                return redirect("/user/login")
            




@app.route("/user/login",methods=['POST',"GET"])
def login():
    if current_user.is_authenticated : 
        return redirect("/user/dashboard")
    else :
        if request.method == 'GET' : 
            return render_template("/user/login.html")
        else : 
            username = request.form.get("username")
            password = request.form.get("password")

            user = User.query.filter(User.username == username).first()
            if user != None :
                if sha256_crypt.verify(password , user.password) :
                    flash("success","سلام ، خوش اومدی . ")
                    return redirect("/")
                else :
                    flash("error",'مشکلی پیش آمده دوباره تلاش کنید . ')
                    return redirect("/user/login")
            else :
                flash("error",'حسابی وجود ندارد ، یکی بساز . ')
                return redirect("/user/sign-up")