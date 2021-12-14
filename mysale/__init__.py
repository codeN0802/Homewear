from flask import Flask
from flask_sqlalchemy import SQLAlchemy
import cloudinary
from flask_login import LoginManager
from flask_mail import Mail, Message
app = Flask(__name__)
app.secret_key = '334%dfsg345F^%#$####$%%^dfgGY' #crud du lieu

app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:12345678@localhost/labsaledb?charset=utf8mb4'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] =True

app.config['PAGE_SIZE'] = 8
db = SQLAlchemy(app=app)

cloudinary.config(
  cloud_name = "dn8gvatsu",
  api_key = "932217124943281",
  api_secret = "jxg3UHnXKjzZqG_sUtTON7DmDr0"
)



login = LoginManager(app=app)

app.config['MAIL_SERVER']='smtp.gmail.com'
app.config['MAIL_PORT'] = 465
app.config['MAIL_USERNAME'] = 'nghinguyen08022000@gmail.com'
app.config['MAIL_PASSWORD'] = 'nghi0802'
app.config['MAIL_USE_TLS'] = False
app.config['MAIL_USE_SSL'] = True
mail = Mail(app)