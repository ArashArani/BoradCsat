#کتاب  خانه ها 

from flask import Flask , render_template ,flash , redirect , url_for

from flask_wtf.csrf import CSRFProtect

from flask_login import LoginManager

from flask_migrate import Migrate


#فایل ها 


from blueprints.admin import app as admin

from blueprints.general import app as general


from models.user import User

from config import SECRET_KEY , SQLALCHEMY_DATABASE_URI

from extentions import db , mail

#ریجستر ها

app = Flask(__name__)


app.register_blueprint(admin)

app.register_blueprint(general)

#کد ها 

app.config["SQLALCHEMY_DATABASE_URI"] = SQLALCHEMY_DATABASE_URI

app.config["SECRET_KEY"] = SECRET_KEY

app.config['MAIL_SERVER'] = 'mail.chabokan.net'

app.config['MAIL_PORT'] = 587

app.config['MAIL_USE_TLS'] = True

app.config['MAIL_USERNAME'] = 'info@noorarose.ir'

app.config['MAIL_PASSWORD'] = 'sWfLvLbtBnpV'

app.config['MAIL_DEFAULT_SENDER'] = 'info@noorarose.ir'

db.init_app(app)

csrf = CSRFProtect(app)

login_manager = LoginManager()

login_manager.init_app(app)

migrate = Migrate(app , db)

mail.init_app(app)

@login_manager.user_loader
def load_user(user_id):
    return User.query.filter(User.id == user_id).first()

@login_manager.unauthorized_handler
def unauthorized ():
    flash ('error','For Use Our Website Please Log in To Your Account')
    return redirect(url_for('user.login'))

with app.app_context():
    db.create_all()
    
'''    
@app.errorhandler(404)
def not_found(error):
    return render_template('404.html') , 404


@app.errorhandler(403)
def abort(error):
    return render_template('403.html') , 403


'''
if __name__ == "__main__":
    app.run(debug=True , host='0.0.0.0')