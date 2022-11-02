import controllers.chat
from decorators.authentication import login_required
from flask import Blueprint, session

chat_router = Blueprint('chat_router', __name__)

@chat_router.route("/chat_all")
@login_required
def chat_all():
    return controllers.chat.chat_all(session['id'])

@chat_router.route("/message_user/<int:receiver_id>")
@login_required
def message_user(receiver_id):
    return controllers.chat.message_user(receiver_id)
@chat_router.route("/send_message/<int:receiver_id>")
@login_required
def send_message(sender_id,receiver_id):
    return controllers.chat.send_message(sender_id,receiver_id)
