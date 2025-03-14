from flask import Blueprint , session , request , abort , redirect , render_template , flash , url_for , jsonify

from flask_login import current_user

import os


from config import ADMIN_PASSWORD , ADMIN_USERNAME

from models.user import User

from models.cart import *

from models.cart_item import CartItem

from models.card import Card

from models.course import *

app = Blueprint('general',__name__)

