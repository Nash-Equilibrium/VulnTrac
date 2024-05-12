from flask_login import UserMixin
from init import db
from datetime import datetime
from flask_login import LoginManager


def get_user(user_id):
    user = User.query.filter_by(id=user_id).first()
    return user


# File表
class File(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    file_name = db.Column(db.String(100), nullable=False)
    file_type = db.Column(db.String(10), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey("user.id"))
    created_at = db.Column(db.DateTime, default=datetime.now)


# User表
class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), nullable=False)
    password = db.Column(db.String(20), nullable=False)
    email = db.Column(db.String(50), nullable=False)
    role = db.Column(db.String(10), nullable=False)  # 0:普通用户 1:管理员
    created_at = db.Column(db.DateTime, default=datetime.now)
    updated_at = db.Column(db.DateTime, default=datetime.now)


# Analysis表
class Analysis(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    file_id = db.Column(db.Integer, db.ForeignKey("file.id"))
    result = db.Column(db.String(2000), nullable=False)
    status = db.Column(db.String(10), nullable=False)  # 0:未处理 1:处理中 2:处理完成
    created_at = db.Column(db.DateTime, default=datetime.now)
    updated_at = db.Column(db.DateTime, default=datetime.now)


# History表
class History(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("user.id"))
    file_id = db.Column(db.Integer, db.ForeignKey("file.id"))
    analysis_id = db.Column(db.Integer, db.ForeignKey("analysis.id"))
    created_at = db.Column(db.DateTime, default=datetime.now)


# repo表
class Repo(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    repo_name = db.Column(db.String(100), nullable=False)
    repo_url = db.Column(db.String(100), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey("user.id"))
    last_archive_hash = db.Column(db.String(100), nullable=False)
    last_checked_at = db.Column(db.DateTime, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.now)
