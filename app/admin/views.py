from . import admin
from ..models import User, Item, Conversation, Likes
from flask import jsonify, request, url_for, render_template_string
from .. import db
from ..errors import unauthorized, not_found, forbidden, bad_request
from flask_jwt_extended import get_jwt_identity, jwt_required
from flask_mail import Message
from app import mail

# List of all emails linked to Administrative accounts
VALID_ADMIN_EMAILS = ["sr5361@nyu.edu"]


@admin.route("/isAdmin", methods=["GET"])
@jwt_required()
def getInfo():
    email = get_jwt_identity()
    if email in VALID_ADMIN_EMAILS:
        return jsonify({"status": True})
    return jsonify({"status": False})


@admin.route("/getReports", methods=["GET"])
@jwt_required()
def get_reports():
    # Get a list of reports from the database, both reported users and reported items
    email = get_jwt_identity()
    if email not in VALID_ADMIN_EMAILS:
        return bad_request("User does not have administrator privileges")

    usr_report_list = User.query.filter_by(reported=1).all()
    item_report_list = Item.query.filter_by(reported=1).all()
    reports = jsonify({"reported_users": [usr.to_json() for usr in usr_report_list],
                       "reported_items": [item.to_json() for item in item_report_list]})
    return reports


@admin.route("/removeUser", methods=["DELETE"])
@jwt_required()
def remove_user():
    email = get_jwt_identity()
    if email not in VALID_ADMIN_EMAILS:
        return bad_request("User does not have administrator privileges")
    # Remove a user, all of their posts, their chats, reports, anything else related to the user.
    usr_email = request.json["email"]
    user = User.query.filter_by(email=usr_email).first()
    if not user:
        return bad_request("User does not exist")
    # Remove all items related to the user
    items = Item.query.filter_by(email=usr_email).all()
    for item in items:
        db.session.delete(item)

    # Remove all likes related to the user
    likes = Likes.query.filter_by(email=usr_email).all()
    for like in likes:
        db.session.delete(like)

    # Remove all chats related to the user
    conversations1 = Conversation.query.filter_by(email1=usr_email).all()
    conversations2 = Conversation.query.filter_by(email2=usr_email).all()
    conversations = conversations1 + conversations2
    for conversation in conversations:
        db.session.delete(conversation)
    db.session.delete(user)
    db.session.commit()

    #send email notificaiton to the user.
    header = "Your account has been deleted"
    html_message = render_template_string('''
                        <html>
                            <body>
                                <h1>Account Deleted</h1>
                                <p>Your account has been deleted. After review by our 
                                team and from user reports, we have suspended your account 
                                and deleted all data. </p>
                            </body>
                        </html>
                    ''')

    msg = Message(header, recipients=[usr_email], html=html_message)
    mail.send(msg)

    return jsonify({'User deletion': 'Success'})


@admin.route("/removeItem", methods=["DELETE"])
@jwt_required()
def remove_item():
    # Remove an item.
    email = get_jwt_identity()
    if email not in VALID_ADMIN_EMAILS:
        return bad_request("User does not have administrator privileges")

    # Remove a user, all of their posts, their chats, reports, anything else related to the user.
    item_id = request.json["item_id"]
    item = Item.query.filter_by(item_id=item_id).first()
    if not item:
        return bad_request("Item does not exist")
    db.session.delete(item)
    db.session.commit()
    return jsonify({'Item deletion': 'Success'})