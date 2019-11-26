from flask import Flask
from flask_login import LoginManager

from flask_restful import Resource, Api
from flask_cors import *
from flask_sqlalchemy import SQLAlchemy


app = Flask(__name__)
api = Api(app)
CORS(app, supports_credentials=True)

db = SQLAlchemy(app)

from app import views, models


# 初始化db,并创建models中定义的表格
#with app.app_context(): # 添加这一句，否则会报数据库找不到application和context错误
db.init_app(app) # 初始化db
db.create_all() # 创建所有未创建的table


login_manager = LoginManager()

login_manager.init_app(app)
app.secret_key = 'strong_session'
login_manager.session_protection = 'strong_session'
login_manager.login_view = 'login'
login_manager.login_message = 'please login'


@login_manager.user_loader
def load_user(user_id):
    return models.User.get_user(user_id)

#app.run(host='127.0.0.1', port=5000, debug=True)