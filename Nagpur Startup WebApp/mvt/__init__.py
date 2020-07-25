import os
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_login import LoginManager
from flask import Flask, request, url_for
from flask_mail import Mail, Message
from itsdangerous import URLSafeTimedSerializer, SignatureExpired

app = Flask(__name__)
app.config['SECRET_KEY'] = '5791628bb0b13ce0c676dfde280ba245'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///site.db'

app.config['MAIL_SERVER']='smtp.gmail.com'
app.config['MAIL_USERNAME']=''
app.config['MAIL_PASSWORD']=''
app.config['MAIL_DEFAULT_SENDER']=''
app.config['MAIL_PORT']=465
app.config['MAIL_USE_SSL']=True
app.config['MAIL_USE_TLS']=False
app.config['MAIL_DEBUG']=True
app.config['USER_ENABLE_EMAIL'] = True

mail = Mail(app)

s = URLSafeTimedSerializer('S8aGv1VnyUxYqT9jITFe')

PEOPLE_FOLDER = os.path.join('static','img')
app.config['UPLOAD_FOLDER'] = PEOPLE_FOLDER

db = SQLAlchemy(app)
bcrypt = Bcrypt(app)
login_manager = LoginManager(app)
login_manager.login_view = 'login'
login_manager.login_message_category = 'info'

from mvt import routes
