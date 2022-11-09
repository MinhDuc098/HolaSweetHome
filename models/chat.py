from models.model import db  

class Chat(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    user_id_1 = db.Column(db.Integer, db.ForeignKey('user.id'), nullable = False)
    user_id_2 = db.Column(db.Integer, db.ForeignKey('user.id'), nullable = False)

class Message(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    chat_id = db.Column(db.Integer, db.ForeignKey('chat.id'), nullable = False)
    message = db.Column(db.String(1000), unique = False, nullable = False)
    sender_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable = False)
    timestamp = db.Column(db.DateTime, nullable = False)
