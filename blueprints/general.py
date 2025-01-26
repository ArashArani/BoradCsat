from flask import Blueprint , session , request , abort , redirect , render_template , flash , url_for , jsonify

from flask_login import current_user

import os


from config import ADMIN_PASSWORD , ADMIN_USERNAME

from models.category import Category

from models.user import User

from models.cart import *

from models.cart_item import CartItem

from models.card import Card

from models.product import *

app = Blueprint('general',__name__)


@app.route('/')
def main():
    category = Category.query.all()
    product = Product.query.filter(Product.active==1).filter(Product.stock > 0).order_by(desc(Product.id)).all()
    low_stock = Product.query.filter(Product.active==1).order_by(asc(Product.stock)).limit(8).all()
    return render_template('home.html',low_stock = low_stock,product = product,category=category)


@app.route('/products/<name>')
def product_info(name):
    product = Product.query.filter(Product.name == name).filter(Product.stock > 0).filter(Product.active ==1).first_or_404()
    category = Category.query.filter(Category.id == product.category_id).first_or_404()
    related_products = Product.query.filter(Product.category_id == category.id).filter(Product.id != product.id).filter(Product.active==1).filter(Product.stock > 0).order_by(func.random()).limit(4).all()
    return render_template('product-info.html', related_products = related_products,product = product , category = category)

@app.route('/category/<name>')
def category(name):
    page = request.args.get('page', 1, type=int)
    per_page = 12
    c = Category.query.filter(Category.name == name).first_or_404()
    products = Product.query.filter(Product.category_id == c.id).paginate(page=page, per_page=per_page, error_out=False)
    return render_template('products.html',c=c , products = products)



@app.route('/products')
def products():
    page = request.args.get('page', 1, type=int)
    per_page = 1
    products = Product.query.paginate(page=page, per_page=per_page, error_out=False)
    return render_template('products.html', products=products)


@app.route('/search')
def search():
    query = request.args.get('query', '')
    page = request.args.get('page', 1, type=int)
    per_page = 12

    # جستجو در محصولات بر اساس نام
    products = Product.query.filter(Product.name.ilike(f'%{query}%')).filter(Product.active==1).paginate(page=page, per_page=per_page, error_out=False)

    return render_template('search-results.html', products=products, query=query)