from . import api
from ..models import User, Item, Conversation, Likes
from flask import jsonify, request, url_for
from .. import db
from ..errors import unauthorized, not_found, forbidden, bad_request
from flask_jwt_extended import get_jwt_identity, jwt_required
from geopy.distance import geodesic
import random


# TODO: Start writing the api endpoints
# api endpoints:
# get all the posts that the user has created
# Get all the items based on the locality setting that the user has been set with
# Change the locality
# Initiate the chatting system (research more on whether this should be on the api side or on the client side)


@api.route("/like", methods=["POST"])
@jwt_required()
def likeAnItem():
    item_id = request.json["item_id"]

    item = Item.query.filter_by(item_id=item_id).first()

    if item:
        email = get_jwt_identity()
        new_like = Likes(email=email, item_id=item_id)
        db.session.add(new_like)
        db.session.commit()
        return jsonify(new_like.to_json())

    return bad_request("Cannot find a particular item with the given item ID")


@api.route("/reportItem", methods=["PUT"])
@jwt_required()
def reportItem():
    item_id = request.json["item_id"]
    Item.query.filter_by(item_id=item_id).update(dict(reported=1))
    db.session.commit()

    return jsonify({'Reported item': 'Success'})


@api.route("/reportUser", methods=["PUT"])
@jwt_required()
def reportUser():
    email = request.json["email"]
    User.query.filter_by(email=email).update(dict(reported=1))
    db.session.commit()

    return jsonify({'Reported user': 'Success'})


@api.route("/changeLocation", methods=["PUT"])
@jwt_required()
def changeLocation():
    email = get_jwt_identity()
    longitude = request.json["longitude"]
    latitude = request.json["latitude"]
    User.query.filter_by(email=email).update(dict(latitude=latitude, longitude=longitude))
    db.session.commit()

    return jsonify({"Msg": "success"})


@api.route("changeProximity", methods=["PUT"])
@jwt_required()
def changeProximity():
    email = get_jwt_identity()
    proximity = request.json["proximity"]
    User.query.filter_by(email=email).update(dict(proximity=proximity))
    db.session.commit()

    return jsonify({"Msg": "success"})


@api.route("/getItems")
@jwt_required()
def getAppropriateItems():
    def withinDistance(orig_lat, orig_long, dst_lat, dst_long, proximity):  # in miles

        origin = (orig_lat, orig_long)
        dist = (dst_lat, dst_long)

        return geodesic(origin, dist).miles < proximity

    email = get_jwt_identity()
    item_id = request.json["item_id"]

    itemUser = User.query.join(Item, User.email == Item.email).filter(Item.item_id == item_id).first()
    origin_lat = itemUser.latitude
    origin_long = itemUser.longitude
    proximity = itemUser.proximity

    allUser = User.query.all()
    validUsers = []

    for user in allUser:
        if user.email == email:
            continue
        if withinDistance(origin_lat, origin_long, user.latitude, user.longitude, proximity):
            validUsers.append(user.email)

    items = Item.query.filter(Item.email.in_(validUsers)).all()

    return jsonify({"items": [item.to_json() for item in items]})


@api.route("/newPost", methods=["POST"])
@jwt_required()
def newItem():
    email = get_jwt_identity()

    '''
    item_id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(320))
    name = db.Column(db.String(30))
    description = db.Column(db.String(200))
    reported = db.Column(db.Integer)
    '''
    name = request.json["name"]
    description = request.json["description"]
    found_item = 1
    id_ = 1

    while found_item is not None:
        id_ = random.randint(1, 9999)
        found_item = Item.query.filter_by(item_id=id_).first()

    new_item = Item(item_id=id_, email=email, name=name, description=description, reported=0)
    db.session.add(new_item)
    db.session.commit()

    return jsonify(new_item.to_json())



# TODO: JONATHAN
@api.route("/myposts/")
@jwt_required()
def getMyPosts():
    return jsonify({"Hello World!": 1})


#
# #TODO: RISHIKESH
# @api.route("/getItems/")
# @jwt_required()
# def getItems():
#     pass

# @api.route("/changeLocation", methods=["POST"])
# @jwt_required()
# def changeLocation():
#     current_user_email = get_jwt_identity()
#
#     ip_address = request.remote_addr
#     url = f"https://ipinfo.io/{ip_address}/geo"
#     response = requests.get(url)
#     location = response.json()["loc"].split(",")
#     new_latitude = location[0]
#     new_longitude = location[1]
#
#     user = User.query.filter_by(email=current_user_email).first()
#     if not user:
#         return not_found('User not found')
#
#     user.latitude = new_latitude
#     user.longitude = new_longitude
#     db.session.commit()
#
#     return jsonify({'message': 'Latitude and longitude updated successfully'})
