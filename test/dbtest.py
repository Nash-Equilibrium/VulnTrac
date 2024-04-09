from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()


class File(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    filename = db.Column(db.String(100), nullable=False)
    type = db.Column(db.String(10), nullable=False)


class Text(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    filename = db.Column(db.String(100), nullable=False)
    type = db.Column(db.String(10), nullable=False)


db.create_all()

file_db = File(filename="test", type="txt")
db.session.add(file_db)
db.session.commit()
