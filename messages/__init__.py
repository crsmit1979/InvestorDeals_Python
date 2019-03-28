from flask import Blueprint, render_template,request, redirect
from models.User import User
from models.Message import Message
from flask_login import  current_user, login_required
from utils import requires_auth

def add_routes(app=None):
    messages_page = Blueprint('messages_page', __name__,
                            template_folder='templates')

    @messages_page.route("/message/<message_to>", methods=['GET'])
    @requires_auth
    def message(message_to):
        user_to = User.get_by_uuid(message_to)
        return render_template("message.html", message_to=user_to, message_from=current_user.uuid)

    @messages_page.route("/reply_email/<id>")
    @requires_auth
    def reply_email(id):
        message = Message.set_message_as_read(id)
        return render_template("reply_email.html", message=message)

    @messages_page.route("/send_message", methods=['POST'])
    @requires_auth
    def send_message():
        email_from = request.form['email_from']
        email_to = request.form['email_to']
        message = request.form['message']
        msg = Message.create(message_from=email_from, message_to=email_to, message=message)
        return redirect("/")



    @messages_page.route("/delete_email/<id>", methods=['GET'])
    @requires_auth
    def delete_email(id):
        Message.delete(id)
        return redirect("/inbox")


    app.register_blueprint(messages_page)
