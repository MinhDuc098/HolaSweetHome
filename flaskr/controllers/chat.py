
from datetime import datetime
from models.user import User
from models.chat import Chat
from models.chat import Message
from models.model import db
from flask import render_template,session

def chat_all(userid):
    #get all the user with userid
    user = User.query.filter(User.id != userid).all()
    return render_template("chat/chat_all.html", list_user = user)

def message_user(receiver_id):
    #get all the user with userid
    sender_id = session['id']
    sender = User.query.filter(User.id == sender_id).first()
    receiver = User.query.filter(User.id == receiver_id).first()
    list_message = get_list_message(sender_id,receiver_id)
    if(list_message == []):
        chat = Chat(user_id_1 = sender_id, user_id_2 = receiver_id)
        db.session.add(chat)
        db.session.commit()
    return render_template("chat/message_user.html", sender = sender, receiver = receiver, list_message = list_message)
def get_list_message(sender_id,receiver_id):
    chat = Chat.query.filter(((Chat.user_id_1 == sender_id) & (Chat.user_id_2 == receiver_id))|( (Chat.user_id_2 == sender_id) & (Chat.user_id_1 == receiver_id))).all()
    #get all message with chat_id == chat.id
    list_message = []
    for c in chat:
        message = Message.query.filter(Message.chat_id == c.id).all()
        list_message.append(message)
    return list_message
def send_message(sender_id,receiver_id):
    #get all the user with userid
    sender = User.query.filter(User.id == sender_id).first()
    receiver = User.query.filter(User.id == receiver_id).first()
    return render_template("chat/send_message.html", sender = sender, receiver = receiver)
