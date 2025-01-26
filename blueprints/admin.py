from flask import Blueprint , session , request , abort , redirect , render_template , flash , url_for

from random import randint

from flask_mail import Message

import os

from extentions import db , mail , generate_random_code

from config import ADMIN_PASSWORD , ADMIN_USERNAME

from models.category import Category

from models.user import User

from models.discount import Discount

from models.cart import *

from models.cart_item import CartItem

from models.card import Card

from models.product import Product


app = Blueprint('admin',__name__)

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
    try:
        user_agent = request.headers.get('User-Agent')
        

        if False:
            pass
        else:
            # ابتدا بررسی متد GET
            if request.method == "GET":
                verify_code = randint(1000, 9999)
                print(verify_code)
                
                # ذخیره کد تأییدیه در session
                session['verify_code'] = str(verify_code)
                return render_template("/admin/login.html")
            # سپس بررسی متد POST
            elif request.method == "POST":
                username = request.form.get('username', None)
                password = request.form.get('password', None)
                verify = request.form.get('verify')

                if username == ADMIN_USERNAME and password == ADMIN_PASSWORD and verify == session.get('verify_code'):
                    session['admin_login'] = username
                    flash('success', "Welcome Back Boss !")
                    return redirect('/admin/dashboard')
                else:
                    flash('error', 'Oops Something Went Wrong Try Again . . . ')
                    # تولید کد تأییدیه جدید
                    session['verify_code'] = str(randint(1000, 9999))
                    return redirect('/admin/login')

    except Exception as e:
        print(f"Error: {e}")  # لاگ خطا
        return abort(500)
    





@app.route('/admin/dashboard')
def dashboard():
    try :
        
        product_count = Product.query.count()
        paid_count = Cart.query.filter(Cart.status == 'Verify').count()
        user_count = User.query.count()
        product_list = Product.query.all()
        cart_list = Cart.query.filter(Cart.status == 'Verify').order_by(desc(Cart.id)).limit(5).all()
        top_users = db.session.query(
        User.email.label('user_mail'),
        User.id.label('id'),
        func.count(Cart.id).label('purchase_count'),
        func.sum(CartItem.final_price * CartItem.quantity).label('total_spent')).join(Cart, User.id == Cart.user_id) \
        .join(CartItem, Cart.id == CartItem.cart_id) \
        .filter(or_(Cart.status == 'In Progress' , Cart.status == 'Delivered' )) \
        .group_by(User.id) \
        .order_by(func.count(Cart.id).desc()) \
        .limit(4) \
        .all()
        top_products = db.session.query(
        Product.id.label('product_id'),
        Product.name.label('product_name'),
        func.sum(CartItem.quantity).label('total_sold'),
        func.sum(CartItem.final_price * CartItem.quantity).label('total_revenue')
        ).join(CartItem, Product.id == CartItem.product_id) \
        .join(Cart, CartItem.cart_id == Cart.id) \
        .filter(or_(Cart.status == 'In Progress', Cart.status == 'Delivered')) \
        .group_by(Product.id) \
        .order_by(func.sum(CartItem.quantity).desc()) \
        .limit(4) \
        .all()
        total_sales = db.session.query(
            func.sum(CartItem.final_price * CartItem.quantity).label('total_revenue')
        ).select_from(CartItem) \
        .join(Cart, CartItem.cart_id == Cart.id) \
        .join(Product, CartItem.product_id == Product.id) \
        .filter(or_(Cart.status == 'In Progress', Cart.status == 'Delivered')) \
        .scalar() or 0


        return render_template('/admin/dashboard.html',product_count=product_count,paid_count=paid_count,
                            user_count=user_count,total_sales = total_sales ,
                            product_list = product_list , cart_list = cart_list , top_users = top_users ,top_products = top_products)
    
    except:
        return abort(501)
    
@app.route('/admin/dashboard/products',methods=['GET','POST'])
def products():
        
        if request.method == 'GET':

            products_count = Product.query.count()
            products_active = Product.query.filter(Product.active == 1).count()
            products_notactive = Product.query.filter(Product.active == 0).count()
            total_sales = db.session.query(
            func.sum(CartItem.price * CartItem.quantity).label('total_revenue')
            ).select_from(CartItem) \
            .join(Cart, CartItem.cart_id == Cart.id) \
            .join(Product, CartItem.product_id == Product.id) \
            .filter(or_(Cart.status == 'In Progress', Cart.status == 'Delivered')) \
            .scalar()  or 0
            category= Category.query.all()

            products_list = Product.query.order_by(desc(Product.id)).all()

            return render_template('/admin/products.html', category=category ,products_count=products_count , products_active = products_active , 
                                products_list = products_list , total_sales= total_sales , products_notactive = products_notactive)
    
        else:
            name = request.form.get('name')
            stock = request.form.get('stock')

            price = int(request.form.get('price'))
            discount = int(request.form.get('discount',None))
            descr = request.form.get('descr')
            active = request.form.get('active')
            category_id = request.form.get('category')
            pic1 = request.files.get('pic1')
            pic2 = request.files.get('pic2')

            if discount == None or '':
                discount = 0

            final_price = price - (price*(discount/100))
            final_price = int(final_price)
            discount_price = int(price * (discount/100))
            p = Product(name=name,price=price,descr=descr, discount = discount , discount_price = discount_price ,
                        final_price = final_price , stock=stock ,category_id = category_id)
            if active != '':
                p.active = 1

            else:
                p.active = 0

            pic1.save(f'static/covers/products/{name}1.webp')        
            pic2.save(f'static/covers/products/{name}2.webp')    

            flash('success',f'{name} Add To Your Store .')

            db.session.add(p)
            db.session.commit()   

            return redirect('/admin/dashboard/products') 
    
    

@app.route('/admin/dashboard/products/<int:id>',methods=['GET','POST'])
def edit_products(id):
    try:
        product = Product.query.filter(Product.id == id).first_or_404()

        if request.method == 'GET':
            total_sales = db.session.query(
                func.sum(CartItem.price * CartItem.quantity).label('total_revenue')
            ).select_from(CartItem) \
                .join(Cart, CartItem.cart_id == Cart.id) \
                .join(Product, CartItem.product_id == Product.id) \
                .filter(
                    or_(Cart.status == 'In Progress', Cart.status == 'Delivered'),
                    CartItem.product_id == product.id  # اضافه کردن شرط برای محصول خاص
                ) \
                .scalar() or 0
            products_count = Product.query.count()
            products_active = Product.query.filter(Product.active == 1).count()
            products_notactive = Product.query.filter(Product.active == 0).count()
            category= Category.query.all()

            return render_template('/admin/edit-product.html',total_sales = total_sales , 
                                products_active = products_active , products_count = products_count,
                                products_notactive = products_notactive , category = category , product = product)
        else:
            name = request.form.get('name')
            price = int(request.form.get('price'))
            discount = int(request.form.get('discount',None))
            descr = request.form.get('descr')
            active = request.form.get('active')
            category_id = request.form.get('category')
            pic1 = request.files.get('pic1')
            stock = request.form.get('stock')
            pic2 = request.files.get('pic2')


            product.name = name
            product.stock = stock
            product.price = price
            product.discount = discount
            product.descr = descr
            
            product.category_id = category_id
            if discount == None or '':
                discount = 0

            final_price = price - (price*(discount/100))
            

            product.final_price = int(final_price)
            discount_price = int(price * (discount/100))
            product.discount_price = discount_price

            if active != None :
                product.active = 1
            else:
                product.active = 0

            if pic1.filename != '' or None :
                os.remove(f'static/covers/products/{product.name}1.webp')
                pic1.save(f'static/covers/products/{name}1.webp')
            if pic2.filename != '' or None :
                os.remove(f'static/covers/products/{product.name}2.webp')
                pic2.save(f'static/covers/products/{name}2.webp')
            flash('success','The Changes Have Been Successfully Saved.')
            db.session.commit()
            return redirect('/admin/dashboard/products')
    except:
        return abort(501)
@app.route('/delete-product')
def delete_product():
    try : 
        id = request.args.get('id')
        p = Product.query.filter(Product.id == id).first()
        os.remove(f'static/covers/products/{p.name}1.webp')
        os.remove(f'static/covers/products/{p.name}2.webp')

        db.session.delete(p)
        db.session.commit()
        flash('success',f'{p.name} Have Been Deleted Successfuly . ')
        return redirect('/admin/dashboard/products')
    
    except:
        return abort(501)


@app.route('/admin/dashboard/category',methods=['GET','POST'])
def category():
    try:
        if request.method == 'GET':
            products_count = Category.query.count()
            products_active = Product.query.filter(Product.active == 1).count()
            products_notactive = Product.query.filter(Product.active == 0).count()
            total_sales = db.session.query(
            func.sum(CartItem.price * CartItem.quantity).label('total_revenue')
            ).select_from(CartItem) \
            .join(Cart, CartItem.cart_id == Cart.id) \
            .join(Product, CartItem.product_id == Product.id) \
            .filter(or_(Cart.status == 'In Progress', Cart.status == 'Delivered')) \
            .scalar() or 0
            category= Category.query.order_by(desc(Category.id)).all()

            return render_template('/admin/category.html' , category= category ,products_count=products_count , products_active = products_active 
                                        , total_sales= total_sales , products_notactive = products_notactive)
        else:

            name = request.form.get('name')
            pic = request.files.get('pic')

            c = Category(name = name)
            pic.save(f'static/covers/category/{c.name}.webp')
            db.session.add(c)
            db.session.commit()

            flash('success',f'{name} Have Been Successfily Added . ')
            return redirect('/admin/dashboard/category')
    
    except:
        return abort(501)
    

@app.route('/admin/dashboard/category/<int:id>',methods=['GET','POST'])
def edit_category(id):
    try:
        category = Category.query.filter(Category.id == id).first_or_404()

        if request.method == 'GET':
            products_count = Category.query.count()
            products_active = Product.query.filter(Product.active == 1).count()
            products_notactive = Product.query.filter(Product.active == 0).count()
            total_sales = db.session.query(
                func.sum(CartItem.price * CartItem.quantity).label('total_revenue')
                ).select_from(CartItem) \
                .join(Cart, CartItem.cart_id == Cart.id) \
                .join(Product, CartItem.product_id == Product.id) \
                .filter(or_(Cart.status == 'In Progress', Cart.status == 'Delivered')) \
                .scalar()  or 0

            return render_template('/admin/edit-category.html' , category= category ,products_count=products_count , products_active = products_active 
                                            , total_sales= total_sales , products_notactive = products_notactive)
        

        else : 
            name = request.form.get('name')
            pic = request.files.get('pic')
            category.name = name

            if pic.filename != '' or None:
                os.remove(f'static/covers/category/{category.name}.webp')
                pic.save(f'static/covers/category/{name}.webp')

            flash('success','The Changes Have Been Successfully Saved.')

            db.session.commit()

            return redirect('/admin/dashboard/category')
    except:
        return abort(501)
    

@app.route('/delete-category')
def delete_category():
    id = request.args.get('id')
    c = Category.query.filter(Category.id == id).first_or_404()
    Product.query.filter(Product.category_id == c.id).update({Product.category_id: None})
    os.remove(f'static/covers/category/{c.name}.webp')
    db.session.delete(c)
    db.session.commit()

    flash('success',f'{c.name} Have Been Successfuly Deleted .')

    return redirect('/admin/dashboard/category')

@app.route('/admin/dashboard/cards',methods=['POST','GET'])
def card():
    try : 
        if request.method == 'GET':
            products_count = Card.query.count()
            products_active = Card.query.filter(Card.status == 'ON').count()
            products_notactive = Card.query.filter(Card.status == 'OFF').count()
            cards = Card.query.order_by(desc(Card.id)).all()
            total_sales = db.session.query(
                func.sum(CartItem.price * CartItem.quantity).label('total_revenue')
            ).select_from(CartItem) \
            .join(Cart, CartItem.cart_id == Cart.id) \
            .join(Product, CartItem.product_id == Product.id) \
            .filter(or_(Cart.status == 'In Progress', Cart.status == 'Delivered')) \
            .scalar() or 0

            return render_template('/admin/card.html',total_sales=total_sales ,cards=cards ,products_notactive =products_notactive ,
                                products_active= products_active ,products_count=products_count )
        else:
            account_name = request.form.get('account_name')
            sort_code = request.form.get('sort_code')
            account_number = request.form.get('account_number')
            status = request.form.get('status')

            c = Card(account_name = account_name , sort_code = sort_code , account_number = account_number , status = status) 
            
            
            flash('success','New Card Have Been Successfily Added . ')
            db.session.add(c)
            db.session.commit()
            return redirect('/admin/dashboard/cards')
    except:
        return abort(501)
    
@app.route('/admin/dashboard/cards/<int:id>',methods=['POST','GET'])
def edit_card(id):

    try:
    
        card = Card.query.filter(Card.id == id).first_or_404()
        if request.method == 'GET':
            products_count = Card.query.count()
            products_active = Card.query.filter(Card.status == 'ON').count()
            products_notactive = Card.query.filter(Card.status == 'OFF').count()
                    
            total_sales = db.session.query(
                    func.sum(CartItem.price * CartItem.quantity).label('total_revenue')
                    ).select_from(CartItem) \
                    .join(Cart, CartItem.cart_id == Cart.id) \
                    .join(Product, CartItem.product_id == Product.id) \
                    .filter(or_(Cart.status == 'In Progress', Cart.status == 'Delivered')) \
                    .scalar() or 0
            return render_template('/admin/edit-card.html',total_sales=total_sales ,card=card ,products_notactive =products_notactive ,
                                        products_active= products_active ,products_count=products_count )
        else:

            account_name = request.form.get('account_name')
            sort_code = request.form.get('sort_code')
            account_number = request.form.get('account_number')
            status = request.form.get('status')

            card.account_name = account_name
            card.sort_code = sort_code
            card.account_number = account_number
            card.status = status

            flash('success','The Changes Have Been Successfully Saved.')
            db.session.commit()
            return redirect('/admin/dashboard/cards')
    except:
        return abort(501)


@app.route('/delete-card')
def delete_card():
    id = request.args.get('id')
    c = Card.query.filter(Card.id == id).first()
    flash('success',f'{c.account_name} Have Been Successfuly Deleted .')
    db.session.delete(c)
    db.session.commit()
    return redirect('/admin/dashboard/cards')


@app.route('/admin/dashboard/carts')
def carts():
    paid_count = Cart.query.filter(Cart.status == 'Verify').count()
    user_count = User.query.count()
    product_count = Product.query.count()

    verify_carts = Cart.query.filter(Cart.status == 'Verify').all()
    in_progress_carts = Cart.query.filter(Cart.status == 'In Progress').all()
    delivered_carts = Cart.query.filter(Cart.status == 'Delivered').all()
    rejected_carts = Cart.query.filter(Cart.status == 'Rejected').all()
    returned_carts = Cart.query.filter(Cart.status == 'Returned').all()


                    
    total_sales = db.session.query(
                    func.sum(CartItem.price * CartItem.quantity).label('total_revenue')
                    ).select_from(CartItem) \
                    .join(Cart, CartItem.cart_id == Cart.id) \
                    .join(Product, CartItem.product_id == Product.id) \
                    .filter(or_(Cart.status == 'In Progress', Cart.status == 'Delivered')) \
                    .scalar() or 0

    if request.method =='GET':
        return render_template('/admin/carts.html' , paid_count = paid_count ,total_sales = total_sales,
                                user_count = user_count, delivered_carts = delivered_carts ,verify_carts = verify_carts ,
                                in_progress_carts = in_progress_carts ,product_count = product_count ,
                                rejected_carts = rejected_carts , returned_carts = returned_carts)   




@app.route('/admin/dashboard/carts/<int:id>',methods=['POST','GET'])
def edit_carts(id):
    cart = Cart.query.filter(Cart.id == id).first_or_404()
    paid_count = Cart.query.filter(Cart.status == 'Verify').count()
    user_count = User.query.count()
    product_count = Product.query.count()

                    
    total_sales = db.session.query(
                    func.sum(CartItem.price * CartItem.quantity).label('total_revenue')
                    ).select_from(CartItem) \
                    .join(Cart, CartItem.cart_id == Cart.id) \
                    .join(Product, CartItem.product_id == Product.id) \
                    .filter(or_(Cart.status == 'In Progress', Cart.status == 'Delivered')) \
                    .scalar() or 0

    if request.method =='GET':
        return render_template('/admin/edit-cart.html',cart = cart , paid_count = paid_count ,total_sales = total_sales,
                                user_count = user_count , product_count = product_count)
    else:
        status = request.form.get('status')
        if status == 'Rejected' :
            for cart_item in cart.cart_items:
                product = cart_item.product
                product.stock += cart_item.quantity  # Decrease stock by the quantity purchased
                
                if product.stock > 0:
                    product.active = 1
        
        if status == 'In Progress' :
            d = Discount()
            d.user_id = cart.user.id
            d.status = 'Not Used'
            total = int(cart.final_price())
            price = (total * 10)/100
            price = int(price)
            d.code = generate_random_code()
            d.amount = price
            db.session.add(d)



            msg = Message('Status Of Your Payment',recipients=[cart.user.email])
            if cart.user.f_name == 'None':
                msg.body= f'Dear {cart.user.email} , your payment has been confirmed. The products will be delivered to you in the coming days. Thank You! \nPro Pharma Labz UK'
            else:
                msg.body= f'Dear {cart.user.f_name} , your payment has been confirmed. The products will be delivered to you in the coming days. Thank You! \nPro Pharma Labz UK'

            #mail.send(msg)

        elif status == 'Deliverd' :
            msg = Message('Status Of Your Payment',recipients=[cart.user.email])

            if cart.user.f_name == 'None':
                msg.body = f'Dear {cart.user.email}, your payment has been confirmed. Your order has been dispatched and will be delivered to you in the coming days. Thank You! \nPro Pharma Labz UK'
            else:
                msg.body = f'Dear {cart.user.f_name}, your payment has been confirmed. Your order has been dispatched and will be delivered to you in the coming days. Thank You! \nPro Pharma Labz UK'
            #mail.send(msg)


        elif status == 'Rejected':
            msg = Message('Status Of Your Payment',recipients=[cart.user.email])

            if cart.user.f_name == 'None':
                msg.body = f'Dear {cart.user.email}, unfortunately, your payment has been rejected. Please check your payment details and try again. Thank You! \nPro Pharma Labz UK'
            else:
                msg.body = f'Dear {cart.user.f_name}, unfortunately, your payment has been rejected. Please check your payment details and try again. Thank You! \nPro Pharma Labz UK'
            #mail.send(msg)
        
        
        cart.status = status
        flash('success','The status of the cart has changed.')
        db.session.commit()
        return redirect('/admin/dashboard/carts')
    

@app.route('/admin/dashboard/verify-carts')
def verfiy_carts():
    cart = Cart.query.filter(Cart.status == 'Verify').all()
    status = 'Verfiy'

    paid_count = Cart.query.filter(Cart.status == 'Verify').count()
    user_count = User.query.count()
    product_count = Product.query.count()
    total_sales = db.session.query(
                    func.sum(CartItem.price * CartItem.quantity).label('total_revenue')
                    ).select_from(CartItem) \
                    .join(Cart, CartItem.cart_id == Cart.id) \
                    .join(Product, CartItem.product_id == Product.id) \
                    .filter(or_(Cart.status == 'In Progress', Cart.status == 'Delivered')) \
                    .scalar() or 0
    
    return render_template('/admin/cart-status.html',cart = cart , paid_count = paid_count , 
                           user_count = user_count , product_count = product_count , total_sales = total_sales ,
                           status = status)

@app.route('/admin/dashboard/in-progress-carts')
def in_progress_carts():
    cart = Cart.query.filter(Cart.status == 'In Progress').all()
    status = 'In Progress'

    paid_count = Cart.query.filter(Cart.status == 'Verify').count()
    user_count = User.query.count()
    product_count = Product.query.count()
    total_sales = db.session.query(
                    func.sum(CartItem.price * CartItem.quantity).label('total_revenue')
                    ).select_from(CartItem) \
                    .join(Cart, CartItem.cart_id == Cart.id) \
                    .join(Product, CartItem.product_id == Product.id) \
                    .filter(or_(Cart.status == 'In Progress', Cart.status == 'Delivered')) \
                    .scalar() or 0
    
    return render_template('/admin/cart-status.html',cart = cart , paid_count = paid_count , 
                           user_count = user_count , product_count = product_count , total_sales = total_sales ,
                           status = status)



@app.route('/admin/dashboard/delivered-carts')
def delivered_carts():
    cart = Cart.query.filter(Cart.status == 'Delivered').all()
    status = 'Delivered'

    paid_count = Cart.query.filter(Cart.status == 'Verify').count()
    user_count = User.query.count()
    product_count = Product.query.count()
    total_sales = db.session.query(
                    func.sum(CartItem.price * CartItem.quantity).label('total_revenue')
                    ).select_from(CartItem) \
                    .join(Cart, CartItem.cart_id == Cart.id) \
                    .join(Product, CartItem.product_id == Product.id) \
                    .filter(or_(Cart.status == 'In Progress', Cart.status == 'Delivered')) \
                    .scalar() or 0
    
    return render_template('/admin/cart-status.html',cart = cart , paid_count = paid_count , 
                           user_count = user_count , product_count = product_count , total_sales = total_sales ,
                           status = status)


@app.route('/admin/dashboard/returned-carts')
def returned_carts():
    cart = Cart.query.filter(Cart.status == 'Returned').all()
    status = 'Returned'

    paid_count = Cart.query.filter(Cart.status == 'Verify').count()
    user_count = User.query.count()
    product_count = Product.query.count()
    total_sales = db.session.query(
                    func.sum(CartItem.price * CartItem.quantity).label('total_revenue')
                    ).select_from(CartItem) \
                    .join(Cart, CartItem.cart_id == Cart.id) \
                    .join(Product, CartItem.product_id == Product.id) \
                    .filter(or_(Cart.status == 'In Progress', Cart.status == 'Delivered')) \
                    .scalar() or 0
    
    return render_template('/admin/cart-status.html',cart = cart , paid_count = paid_count , 
                           user_count = user_count , product_count = product_count , total_sales = total_sales ,
                           status = status)



@app.route('/admin/dashboard/rejected-carts')
def rejected_carts():
    cart = Cart.query.filter(Cart.status == 'Rejected').all()
    status = 'Rejected'

    paid_count = Cart.query.filter(Cart.status == 'Verify').count()
    user_count = User.query.count()
    product_count = Product.query.count()
    total_sales = db.session.query(
                    func.sum(CartItem.price * CartItem.quantity).label('total_revenue')
                    ).select_from(CartItem) \
                    .join(Cart, CartItem.cart_id == Cart.id) \
                    .join(Product, CartItem.product_id == Product.id) \
                    .filter(or_(Cart.status == 'In Progress', Cart.status == 'Delivered')) \
                    .scalar() or 0
    
    return render_template('/admin/cart-status.html',cart = cart , paid_count = paid_count , 
                           user_count = user_count , product_count = product_count , total_sales = total_sales ,
                           status = status)



@app.route('/admin/dashboard/campain',methods=['GET','POST'])
def campain():
    paid_count = Cart.query.filter(Cart.status == 'Verify').count()
    user_count = User.query.count()
    product_count = Product.query.count()
    total_sales = db.session.query(
                    func.sum(CartItem.price * CartItem.quantity).label('total_revenue')
                    ).select_from(CartItem) \
                    .join(Cart, CartItem.cart_id == Cart.id) \
                    .join(Product, CartItem.product_id == Product.id) \
                    .filter(or_(Cart.status == 'In Progress', Cart.status == 'Delivered')) \
                    .scalar() or 0
    if request.method == 'GET':
        return render_template('/admin/campain.html' , paid_count = paid_count , 
                            user_count = user_count , product_count = product_count , total_sales = total_sales )
    else :
        subject = request.form.get('subject')
        text = request.form.get('text')
        users = User.query.all()
        for i in users:
            msg = Message(subject , recipients=[i.email])
            msg.body = text
            print('send')
            #mail.send(msg)
        flash('success','Your Email Send To All Customers . ')
        return redirect('/admin/dashboard/campain')




@app.route('/admin/dashboard/customers')
def customers():
    paid_count = Cart.query.filter(Cart.status == 'Verify').count()
    user_count = User.query.count()
    product_count = Product.query.count()
    total_sales = db.session.query(
                    func.sum(CartItem.price * CartItem.quantity).label('total_revenue')
                    ).select_from(CartItem) \
                    .join(Cart, CartItem.cart_id == Cart.id) \
                    .join(Product, CartItem.product_id == Product.id) \
                    .filter(or_(Cart.status == 'In Progress', Cart.status == 'Delivered')) \
                    .scalar() or 0
    top_users = db.session.query(
        User.email.label('user_mail'),
        User.id.label('id'),
        func.count(Cart.id).label('purchase_count'),
        func.sum(CartItem.final_price * CartItem.quantity).label('total_spent')).join(Cart, User.id == Cart.user_id) \
        .join(CartItem, Cart.id == CartItem.cart_id) \
        .filter(or_(Cart.status == 'In Progress' , Cart.status == 'Delivered' )) \
        .group_by(User.id) \
        .order_by(func.count(Cart.id).desc()) \
        .limit(10) \
        .all()
    users = User.query.all()

    return render_template('/admin/customers.html',paid_count=paid_count , user_count=user_count , users = users , product_count=product_count 
    , total_sales =  total_sales , top_users = top_users)




@app.route('/admin/dashboard/customers/<int:id>')
def customers_info(id):
    user = User.query.filter(User.id == id).first_or_404()
    paid_count = Cart.query.filter(Cart.status == 'Verify').count()
    user_count = User.query.count()
    product_count = Product.query.count()
    total_sales = db.session.query(
                    func.sum(CartItem.price * CartItem.quantity).label('total_revenue')
                    ).select_from(CartItem) \
                    .join(Cart, CartItem.cart_id == Cart.id) \
                    .join(Product, CartItem.product_id == Product.id) \
                    .filter(or_(Cart.status == 'In Progress', Cart.status == 'Delivered')) \
                    .scalar() or 0
    return render_template('/admin/customers-info.html',paid_count=paid_count , user_count=user_count , user = user , product_count=product_count 
    , total_sales =  total_sales)


@app.route('/admin/dashboard/customers/<int:id>/send-email',methods=['POST','GET'])
def send_email(id):

    user = User.query.filter(User.id == id).first_or_404()
    paid_count = Cart.query.filter(Cart.status == 'Verify').count()
    user_count = User.query.count()
    product_count = Product.query.count()
    total_sales = db.session.query(
                    func.sum(CartItem.price * CartItem.quantity).label('total_revenue')
                    ).select_from(CartItem) \
                    .join(Cart, CartItem.cart_id == Cart.id) \
                    .join(Product, CartItem.product_id == Product.id) \
                    .filter(or_(Cart.status == 'In Progress', Cart.status == 'Delivered')) \
                    .scalar() or 0
    if request.method == 'GET':
        return render_template('/admin/send-email.html',paid_count=paid_count , user_count=user_count  , product_count=product_count 
        , total_sales =  total_sales)
    else :
        subject = request.form.get('subject')
        text = request.form.get('text')
        msg = Message(subject , recipients=[user.email])
        msg.body = text
        print('send')
            #mail.send(msg)
        flash('success',f'Your Email Send To {user.email} . ')
        return redirect(f'/admin/dashboard/customers/{user.id}')
    
@app.route('/admin/dashboard/customers/<int:id>/add-discount', methods=['GET','POST'])
def add_discount(id):
    user = User.query.filter(User.id == id).first_or_404()
    paid_count = Cart.query.filter(Cart.status == 'Verify').count()
    user_count = User.query.count()
    product_count = Product.query.count()
    total_sales = db.session.query(
                    func.sum(CartItem.price * CartItem.quantity).label('total_revenue')
                    ).select_from(CartItem) \
                    .join(Cart, CartItem.cart_id == Cart.id) \
                    .join(Product, CartItem.product_id == Product.id) \
                    .filter(or_(Cart.status == 'In Progress', Cart.status == 'Delivered')) \
                    .scalar() or 0
    if request.method == 'GET':
        return render_template('/admin/add-discount.html',paid_count=paid_count , user_count=user_count  , product_count=product_count 
        , total_sales =  total_sales)
    else :
        price = request.form.get('price')
        d = Discount()
        d.amount = price
        d.user_id = user.id
        d.status = 'Not Used'
        d.code = generate_random_code()
        msg = Message('You Have New Discount !!!',recipients=[user.email])
        if user.f_name == 'None':
            msg.body = f"Dear {user.email}, Thank you for being a user. \nAs a token of our appreciation, we've added a £ {price} discount to your account.\nYou can find the discount reflected in your user panel."
        else:
            msg.body = f"Dear {user.f_name}, Thank you for being a user. As a token of our appreciation, we've added a £ {price} discount to your account.\nYou can find the discount reflected in your user panel."
        print('SEND')
        #mail.send(msg)

        db.session.add(d)
        db.session.commit()
        flash('success',f'Your Email Send To {user.email} . ')
        return redirect(f'/admin/dashboard/customers/{user.id}')
    


