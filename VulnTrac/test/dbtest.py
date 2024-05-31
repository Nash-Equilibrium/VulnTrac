from flask_sqlalchemy import SQLAlchemy
from flask import Flask
from dotenv import load_dotenv
import os

load_dotenv()
app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = os.getenv("SQLALCHEMY_DATABASE_URI")
db = SQLAlchemy(app)


class File(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    filename = db.Column(db.String(100), nullable=False)
    type = db.Column(db.String(10), nullable=False)


class Text(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    filename = db.Column(db.String(100), nullable=False)
    type = db.Column(db.String(10), nullable=False)


with app.app_context():
    db.create_all()

    file_db = File(filename="test", type="txt")
    db.session.add(file_db)
    db.session.commit()

if __name__ == "__main__":
    app.run(debug=True)
