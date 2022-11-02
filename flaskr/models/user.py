from models.model import db
from models.home import Home


class UserRole():
    MEMBER = "MEMBER"
    ADMIN = "ADMIN"
    BANNED = "BANNED"
    SELLER = "SELLER"


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(120), nullable=False)
    banned = db.Column(db.Boolean, nullable=True, default=False)
    role = db.Column(db.String(80), nullable=False, default=UserRole.MEMBER)
    posts = db.relationship('Post', back_populates="author")
    comments = db.relationship('Comment')
    reports = db.relationship('ReportPost', backref='user', lazy=True)
    reporthomes = db.relationship('ReportHome', backref='user', lazy=True)
    reportUsers = db.relationship('ReportUser', backref='user', lazy=True)
    reportUserDetail = db.relationship(
        'ReportUserDetail', backref='user', lazy=True)
    home = db.relationship('Home', backref='owner', lazy=True)


class Bookmark(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    home_id = db.Column(db.Integer, db.ForeignKey('home.id'), nullable=False)


class RoomRequest(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    content = db.Column(db.String(500), nullable=False)
    timestamp = db.Column(db.DateTime, nullable=False)


class WebsiteFeedback(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    feedback = db.Column(db.String(1000), nullable=False)
    timestamp = db.Column(db.DateTime, nullable=False)


class HomeOwnerRequest(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    home_id = db.Column(db.Integer, db.ForeignKey('home.id'), nullable=False)
    status = db.Column(db.Boolean, nullable=False, default=False)
    user = db.relationship('User')
    home = db.relationship('Home')
