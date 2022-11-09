
from datetime import datetime
from models.user import User
from models.chat import Chat
from models.chat import Message
from models.model import db
from flask import render_template,session, redirect, url_for, flash,request

def chat_all(userid):
    #get all the chat with userid
    chat = Chat.query.filter((Chat.user_id_1 == userid) | (Chat.user_id_2 == userid)).all()
    #list the user chat with userid
    list_user = []
    for c in chat:
        if c.user_id_1 == userid:
            user = User.query.filter(User.id == c.user_id_2).first()
            list_user.append(user)
        else:
            user = User.query.filter(User.id == c.user_id_1).first()
            list_user.append(user)
    #remove duplicate user
    list_user = list(dict.fromkeys(list_user))
    return render_template("chat/chat_all.html", list_user = list_user)

def message_user(receiver_id):
    #get all the user with userid
    sender_id = session['id']
    sender = User.query.filter(User.id == sender_id).first()
    receiver = User.query.filter(User.id == receiver_id).first()
    list_message = get_list_message(sender_id,receiver_id)
    return render_template("chat/message_user.html", sender = sender, receiver = receiver, list_message = list_message)
def get_list_message(sender_id,receiver_id):
    chat = Chat.query.filter(((Chat.user_id_1 == sender_id) & (Chat.user_id_2 == receiver_id))|( (Chat.user_id_2 == sender_id) & (Chat.user_id_1 == receiver_id))).all()
    #get all message with chat_id == chat.id
    list_message = []
    for c in chat:
        message = Message.query.filter(Message.chat_id == c.id).first()
        list_message.append(message)
    return list_message
def send_message(receiver_id):
    #get all the user with userid
    #create a new chats
    sender_id = session['id']
    chat = Chat(user_id_1 = sender_id, user_id_2 = receiver_id)
    db.session.add(chat)
    db.session.commit()
    #create a new message
    message = request.form['message']
    chat_id = chat.id
    sender_id = session['id']
    timestamp = datetime.now()
    message = Message(chat_id = chat_id, message = message, sender_id = sender_id, timestamp = timestamp)
    db.session.add(message)
    db.session.commit()
    sender = User.query.filter(User.id == sender_id).first()
    receiver = User.query.filter(User.id == receiver_id).first()    
    list_message = get_list_message(sender_id,receiver_id)
    return render_template("chat/message_user.html", sender = sender, receiver = receiver, list_message = list_message)
