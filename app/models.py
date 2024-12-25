from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()


class Accounts(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False, unique=True)
    balance = db.Column(db.Float, default=0.0, nullable=False)


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    password = db.Column(db.String(128), nullable=False)
    records = db.relationship('Record', backref='user', lazy=True)
    accounts = db.relationship('Accounts', backref='user', lazy=True)


class Category(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(128), unique=True, nullable=False)
    records = db.relationship('Record', backref='category', lazy=True)


class Record(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    category_id = db.Column(db.Integer, db.ForeignKey('category.id'), nullable=False)
    money_spent = db.Column(db.Float, default=0.0, nullable=False)