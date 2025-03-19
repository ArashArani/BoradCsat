from flask import Blueprint , abort , redirect , render_template , flash , request , url_for

from flask_login import login_required , login_user , logout_user , current_user

from passlib.hash import sha256_crypt

from models.user import User

from models.cart import Cart

from models.cart_item import CartItem

from models.discount import Discount 

from models.course import Course  

from models.card import Card

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
                    login_user(user)
                    return redirect("/user/dashboard")
                else :
                    flash("error",'مشکلی پیش آمده دوباره تلاش کنید . ')
                    return redirect("/user/login")
            else :
                flash("error",'حسابی وجود ندارد ، یکی بساز . ')
                return redirect("/user/sign-up")


@app.route("/user/dashboard")
@login_required
def dashboard():
    verify_count = current_user.carts.filter(Cart.status == 'Verify').count()
    approved_count = current_user.carts.filter(Cart.status == 'Approved').count()
    rejected_count = current_user.carts.filter(Cart.status == 'Rejected').count()
    return render_template("/user/dashboard.html" , rejected_count = rejected_count , approved_count = approved_count , verify_count = verify_count)

@app.route("/user/cart")
@login_required
def cart():
    cart = current_user.carts.filter(Cart.status == 'pending').first()
    return render_template("/user/cart.html",cart = cart)

@app.route("/add-to-cart")
@login_required
def add_to_cart():
    id = request.args.get("id")
    course = Course.query.filter(Course.id == id).first()
    cart = current_user.carts.filter(Cart.status == 'pending').first()
    verify_cart = current_user.carts.filter(Cart.status == 'Verify').first()
    if verify_cart is None :

      
        if cart is None:
            cart = Cart()
            current_user.carts.append(cart)
            db.session.add(cart)

        # بررسی اینکه آیا محصول قبلاً خریداری شده است
        purchased_items = current_user.carts.filter(Cart.status == 'Approved').join(
            CartItem).filter(CartItem.course == course).all()

        if purchased_items:
            flash('error', f'شما قبلاً این محصول را خریداری کرده‌اید و نمی‌توانید دوباره آن را به سبد خرید اضافه کنید.')
            return redirect('/user/cart')

        cart_item = cart.cart_items.filter(CartItem.course == course).first()

        if cart_item is None:
            item = CartItem(quantity=1)
            item.price = course.price
            item.discount_price = course.discount_price
            item.final_price = course.final_price
            item.cart = cart
            item.course = course
            db.session.add(item)
        else:
            flash(
                'error', f'{cart_item.course.name} هم اکنون در سبد خرید می باشد . ')
            return redirect(url_for('user.cart'))

        db.session.commit()
        flash('success', f'{course.name} با موفقیت به سبد خرید اضافه شد . ')

        return redirect('/user/cart')

    else:
        flash('error', 'شما هنوز سبد خرید در انتظار تایید دارید . پس از تایید خرید میتوانید خرید دیگری انجام دهید . ')
        return redirect('/')
    
@app.route("/delete-from-cart")
def delete_from_cart():
    id = request.args.get("id")
    c = CartItem.query.filter(CartItem.id == id).first()
    db.session.delete(c)
    flash('success',f"{c.course.name} با موفقیت حذف شد . ")
    db.session.commit()
    return redirect(url_for("user.cart"))
    
@app.route("/user/payment")
def payment():
    card_count = Card.query.filter(Card.status == 'ON').count()
    if card_count == 1 :
        cart = current_user.carts.filter(Cart.status == 'pending').first()
        card = Card.query.filter(Card.status == 'ON').first()
        return render_template("/user/payment.html",cart = cart , card = card)
    else : 
        flash("error",'در حال حاضر پرداخت اینترنتی با مشکلی مواجه شده . بعدا تلاش کنید . ')
        return redirect(url_for("user.cart"))

@app.route("/verify-payment")
@login_required
def verify_payment():
    id = request.args.get("id")
    cart = Cart.query.filter(Cart.id == id).first()
    cart.status = 'Verify'
    db.session.commit()
    flash("success",'وضعیت سبد خرید تغییر کرد ، به زودی دوره برات ثبت نام میشه . ')
    return redirect(url_for("user.dashboard"))


@app.route('/courses/<name>/<int:id>')
@login_required
def see_video(name, id):

    course = Course.query.filter(Course.name == name).first()

    carts = current_user.carts.filter(Cart.status == 'Approved').all()

    item = None
    for cart in carts:
        item = cart.cart_items.filter(CartItem.course == course).first()
        if item:
            break

    if item is None:
        flash('error', 'شما دانشجو این دوره نیستید.')
        return redirect(f'/course/{course.name}')

    # Retrieve the video based on the ID
    video = CourseVideo.query.filter(CourseVideo.id == id).first()

    # Check if the video exists
    if not video:
        flash('error','ویدئو مورد نظر یافت نشد')
        # Redirect to the courses page
        return redirect(f'/course/{course.name}')

    # Render the video view template
    return render_template('video.html', video=video)

@app.route("/user/orders")
@login_required
def orders():
    cart_list = current_user.carts.filter(Cart.status == "Verify").all()
    verify_count = current_user.carts.filter(Cart.status == 'Verify').count()
    approved_count = current_user.carts.filter(Cart.status == 'Approved').count()
    rejected_count = current_user.carts.filter(Cart.status == 'Rejected').count()
    return render_template("/user/orders.html" , cart_list = cart_list ,rejected_count = rejected_count , approved_count = approved_count , verify_count = verify_count)

@app.route("/user/orders/approved")
@login_required
def approved_orders():
    cart_list = current_user.carts.filter(Cart.status == "Approved").all()
    verify_count = current_user.carts.filter(Cart.status == 'Verify').count()
    approved_count = current_user.carts.filter(Cart.status == 'Approved').count()
    rejected_count = current_user.carts.filter(Cart.status == 'Rejected').count()
    return render_template("/user/orders-approved.html" , cart_list = cart_list ,rejected_count = rejected_count , approved_count = approved_count , verify_count = verify_count)

@app.route("/user/orders/rejected")
@login_required
def rejected_orders():
    cart_list = current_user.carts.filter(Cart.status == "Rejected").all()
    verify_count = current_user.carts.filter(Cart.status == 'Verify').count()
    approved_count = current_user.carts.filter(Cart.status == 'Approved').count()
    rejected_count = current_user.carts.filter(Cart.status == 'Rejected').count()
    return render_template("/user/orders-rejected.html" , cart_list = cart_list ,rejected_count = rejected_count , approved_count = approved_count , verify_count = verify_count)

@app.route("/user/orders/<int:id>")
@login_required
def order_info(id):
    cart = current_user.carts.filter(Cart.id == id).first_or_404()
    return render_template("/user/order-info.html",cart = cart)

@app.route("/user/log-out")
def log_out():
    logout_user()
    flash("success",'با موفقیت خارج شدید . ')
    return redirect("/")