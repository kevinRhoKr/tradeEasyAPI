from . import api
from ..models import User, Item, Conversation, Likes
from flask import jsonify, request, url_for
from .. import db
from ..errors import unauthorized, not_found, forbidden, bad_request
from flask_jwt_extended import get_jwt_identity, jwt_required
from geopy.distance import geodesic
import random
from flask_mail import Message
from app import mail


# TODO: Start writing the api endpoints
# api endpoints:
# get all the posts that the user has created
# Get all the items based on the locality setting that the user has been set with
# Change the locality
# Initiate the chatting system (research more on whether this should be on the api side or on the client side)

@api.route("/hello")
def hello():
    return jsonify({"Hello": "World"})


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
        creator = item.email

        # get all the likes that the creator has liked
        # check whether the items that the creator has liked is my item.

        items = {}
        allItems = Item.query.filter_by(email=email).all()
        for obj in allItems:
            items[obj.item_id] = 0

        creator_likes = Likes.query.filter_by(email=creator).all()

        for like in creator_likes:
            if like.item_id in items:
                # create new conversation! if not already there.
                conv1 = Conversation.query.filter_by(email1=email, email2=creator).first()
                conv2 = Conversation.query.filter_by(email1=creator, email2=email).first()
                print(conv1)
                print(conv2)
                if conv1 is None and conv2 is None:

                    found_Conv = 1
                    id_ = 1

                    while found_Conv is not None:
                        id_ = random.randint(1, 9999)
                        found_Conv = Conversation.query.filter_by(chat_id=id_).first()

                    new_conversation = Conversation(chat_id=id_, email1=email, email2=creator, item_id=item_id)
                    db.session.add(new_conversation)
                    db.session.commit()

                break

        return jsonify({"email": email, "item_id": item_id, "creator": creator})

    return bad_request("Cannot find a particular item with the given item ID")


@api.route("/chats", methods=["GET"])
@jwt_required()
def getAllChats():
    email = get_jwt_identity()

    conv1 = Conversation.query.filter_by(email1=email).all()
    conv2 = Conversation.query.filter_by(email2=email).all()

    lst1 = []
    lst2 = []

    if conv1:
        lst1 = [ch1.to_json() for ch1 in conv1]
    if conv2:
        lst2 = [ch2.to_json() for ch2 in conv2]

    lst1.extend(lst2)

    return jsonify({'chats': lst1})





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
    # item_id = request.json["item_id"]

    itemUser = User.query.filter_by(email=email).first()
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

    allMyLikes = Likes.query.filter_by(email=email).all()
    alreadyLiked = [likes.item_id for likes in allMyLikes]
    items = Item.query.all()
    valids = []

    for item in items:
        if item.email == email or item.email not in validUsers or item.item_id in alreadyLiked:
            continue
        valids.append(item)

    return jsonify({"items": [item.to_json() for item in valids]})


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
    image = request.json["image"]
    found_item = 1
    id_ = 1

    while found_item is not None:
        id_ = random.randint(1, 9999)
        found_item = Item.query.filter_by(item_id=id_).first()

    new_item = Item(item_id=id_, email=email, name=name, description=description, reported=0, image=image)
    db.session.add(new_item)
    db.session.commit()

    return jsonify(new_item.to_json())


# TODO: JONATHAN
@api.route("/myposts/")
@jwt_required()
def getMyPosts():
    email = get_jwt_identity()
    post_list = Item.query.filter_by(email=email).all()
    return jsonify({"myposts": [post.to_json() for post in post_list]})


@api.route("/profile", methods=["POST"])
@jwt_required()
def getProfile():
    email = request.json["email"]
    user = User.query.filter_by(email=email).first()
    fname = user.f_name
    lname = user.l_name

    return jsonify({"lastName": lname, "firstName": fname})
#
#
@api.route('/sendemail', methods=["PUT"])
def sendemail():
    email = request.json["email"]
    header = request.json["header"]
    html_message = request.json["html_message"]
    msg = Message(header, recipients=[email], html=html_message)
    mail.send(msg)
    return jsonify({"Msg": "email sent success"})
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
