from decorators.authentication import login_required
from flask import Blueprint, request, render_template, session,redirect,url_for
from decorators.authentication import login_required
from models.chat import Chat
import controllers.chat
chat_router = Blueprint('chat_router', __name__)

@chat_router.route("/chat_all")
@login_required
def chat_all():
    return controllers.chat.chat_all(session['id'])

@chat_router.route("/message_user/<int:receiver_id>",methods=["POST", "GET"])
@login_required
def message_user(receiver_id):
    if request.method == "POST":
        return controllers.chat.send_message(receiver_id)
    return controllers.chat.message_user(receiver_id)