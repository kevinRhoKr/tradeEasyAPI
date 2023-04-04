from . import admin
from ..models import User, Item, Conversation, Likes
from flask import jsonify, request, url_for
from .. import db
from ..errors import unauthorized, not_found, forbidden, bad_request
from flask_jwt_extended import get_jwt_identity, jwt_required



@admin.route("/getReports", methods=["GET"])
@jwt_required()
def get_reports():
    # Get a list of reports from the database
    pass

@admin.route("/removeUser", methods=["DELETE"])
@jwt_required()
def remove_user():
    # Remove a user, all of their posts, their chats, reports, anything else related to the user.
    pass

@admin.route("/removeItem", methods=["DELETE"])
@jwt_required()
def remove_item():
    # Remove an item.
    pass