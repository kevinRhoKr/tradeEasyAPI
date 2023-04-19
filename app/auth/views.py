from flask import jsonify, request
from ..models import User
from . import auth
from ..errors import bad_request, not_found, unauthorized
from .. import db
from flask_jwt_extended import create_access_token, unset_jwt_cookies, get_jwt_identity, jwt_required


@auth.route('/')
def hello():
    return jsonify({"Hello World!": 1})


@auth.route('/getAll')
def getAll():
    users = User.query.all()
    response = jsonify({"Users": [user.to_json() for user in users]})
    return response


@auth.route("/login", methods=["POST"])
def login_call():
    # print("here");
    email = request.json.get("inputObj").get("email", None)
    password = request.json.get("inputObj").get("password", None)
    # if username != "test" or password != "test":
    #     return jsonify({"msg": "Bad username or password"}), 401

    curr_user = User.query.filter_by(email=email).first()
    if not curr_user:
        return not_found("User not found")

    if not curr_user.verify_password(password):
        return unauthorized("Invalid credentials")

    access_token = create_access_token(identity=email)
    # print(access_token)
    return jsonify(access_token=access_token)


@auth.route("/logout", methods=["POST"])
def logout_call():
    print("before")
    response = jsonify({"msg": "logout successful"})
    print("0", response)
    # print(get_jwt_identity())
    print("1")
    unset_jwt_cookies(response)
    print("2")
    # print(get_jwt_identity())
    print("3")
    return response


@auth.route('/signup', methods=["POST"])
def signUp():
    signUpDetails = request.json.get("register_details")
    '''
    
        {
        "register_details": {
                            "email": email,
                            "password": password,
                            "fname": f_name,
                            "lname": l_name,
                            "latitude": location1,
                            "longitude": location2, 
                            "proximity": proximity
                        }
        }
                        
        '''

    same_email_user = User.query.filter_by(email=signUpDetails.get("email")).first()
    if same_email_user:
        return bad_request("Already existing email")

    user = User()
    user.email = signUpDetails.get("email")
    user.password = signUpDetails.get("password")
    user.f_name = signUpDetails.get("fname")
    user.l_name = signUpDetails.get("lname")
    user.latitude = signUpDetails.get("latitude")
    user.longitude = signUpDetails.get("longitude")
    user.proximity = signUpDetails.get("proximity")

    db.session.add(user)
    db.session.commit()

    return jsonify(user.to_json()), 201
