from models.model import db


class Home(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), unique=False, nullable=False)
    address = db.Column(db.String(100), unique=False, nullable=False)
    description = db.Column(db.String(1000), unique=False, nullable=False)
    total_rooms = db.Column(db.Integer, unique=False, nullable=False)
    available_rooms = db.Column(db.Integer, unique=False, nullable=False)
    timestamp = db.Column(db.DateTime, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    reports = db.relationship('ReportHome', backref='home', lazy=True)


class RoomDetail(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    home_id = db.Column(db.Integer, db.ForeignKey('home.id'), nullable=False)
    room_type = db.Column(db.String(100), unique=False, nullable=False)
    amount = db.Column(db.Integer, unique=False, nullable=False)
    price = db.Column(db.Float, nullable=False)
    description = db.Column(db.String(1000), unique=False, nullable=False)


class RoomImage(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    room_id = db.Column(db.Integer, db.ForeignKey(
        'room_detail.id'), nullable=False)
    image_link = db.Column(db.String(100), unique=False, nullable=False)


class HomeReview(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    home_id = db.Column(db.Integer, db.ForeignKey('home.id'), nullable=False)
    reviewer_id = db.Column(
        db.Integer, db.ForeignKey('user.id'), nullable=False)
    review = db.Column(db.String(1000), unique=False, nullable=False)
    rating = db.Column(db.Integer, unique=False, nullable=False)
    timestamp = db.Column(db.DateTime, nullable=False)
