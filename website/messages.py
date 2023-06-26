import json
from flask import Blueprint, render_template, request, jsonify
from .models import Messages, Users
from . import db
from flask_login import login_required, current_user
from sqlalchemy import desc
# A blueprint of an application means that it stores your urls
messages = Blueprint('messages', __name__)


@messages.route('/createMessage', methods=['GET', 'POST'])
@login_required
def createMessage():
    name = request.form.get('name')
    content = request.form.get('content')
    recipient_username = Users.query.filter_by(id=name).first()
    if request.method == 'POST':
        inbox = Messages(user_id=current_user.id, user_username=current_user.username, recipient_id=name, recipient_username=recipient_username.username,
                         content=content,)
        db.session.add(inbox)
        db.session.commit()
    return render_template("createMessage.html", user=current_user)


@messages.route('/inbox', methods=['GET', 'POST'])
@login_required
def show_messages():
    inbox = Messages.query.filter_by(
        recipient_id=current_user.id).order_by(desc(Messages.date)).all()
    return render_template("inbox.html", inbox=inbox, user=current_user)


@messages.route('/sent', methods=['GET', 'POST'])
@login_required
def show_sent_messages():
    sent = Messages.query.filter_by(
        user_id=current_user.id).order_by(desc(Messages.date)).all()
    return render_template("sent.html", sent=sent, user=current_user)


@messages.route('/delete_message', methods=['GET', 'POST'])
@login_required
def deleteMessage():
    messages = json.loads(request.data)
    MessageId = messages['MessageId']
    messages = Messages.query.get(MessageId)
    if messages:
        db.session.delete(messages)
        db.session.commit()

    return jsonify({})
