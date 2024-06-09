from flask_sqlalchemy import SQLAlchemy
from flask import Flask
from flask_cors import CORS

db = SQLAlchemy()
# Flask配置
app = Flask(__name__)
app.config.from_object("config")
db.init_app(app)
