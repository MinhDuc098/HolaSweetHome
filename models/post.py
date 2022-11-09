from models.model import db
from datetime import datetime


class Post(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.String(1000), unique=False, nullable=False)
    author_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    timestamp = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    author = db.relationship("User", back_populates="posts")
    image = db.relationship('PostImage', back_populates='post', uselist=False)
    upvotes = db.relationship('Upvote', back_populates="post")
    comments = db.relationship('Comment', backref='post', lazy=True)
    reports = db.relationship('ReportPost', backref='post', lazy=True)


class Comment(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    post_id = db.Column(db.Integer, db.ForeignKey('post.id'), nullable=False)
    author_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    content = db.Column(db.String(1000), unique=False, nullable=False)
    timestamp = db.Column(db.DateTime, nullable=False)


class Upvote(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    post_id = db.Column(db.Integer, db.ForeignKey('post.id'), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    post = db.relationship("Post", back_populates="upvotes")


class PostImage(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    post_id = db.Column(db.Integer, db.ForeignKey('post.id'), nullable=False)
    image_link = db.Column(db.String(200), unique=False, nullable=False)
    post = db.relationship('Post', back_populates="image")
