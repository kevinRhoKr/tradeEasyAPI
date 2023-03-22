from . import api
from ..models import User, Item, Conversation
from flask import jsonify, request, url_for
from .. import db
from ..errors import unauthorized, not_found, forbidden, bad_request
from flask_jwt_extended import get_jwt_identity, jwt_required

# TODO: Start writing the api endpoints
# api endpoints:
    # get all the posts that the user has created
    # Get all the items based on the locality setting that the user has been set with
    # Change the locality



    # Initiate the chatting system (research more on whether this should be on the api side or on the client side)



#TODO: JONATHAN
@api.route("/myposts/")
@jwt_required()
def getMyPosts():
    pass


#TODO: RISHIKESH
@api.route("/getItems/")
@jwt_required()
def getItems():
    pass


#TODO: RYAN
@api.route("/changeLocation/")
@jwt_required()
def changeLocation():
    pass


