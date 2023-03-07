from flask import jsonify, request
from ..models import User
from . import auth
from ..errors import bad_request
from .. import db


@auth.route('/')
def hello():
    return jsonify({"Hello World!": 1})


@auth.route('/getAll')
def getAll():
    users = User.query.all()
    response = jsonify({"Users": [user.to_json() for user in users]})
    return response


@auth.route('/signup', methods=["POST"])
def signUp():
    signUpDetails = request.json.get("register_details")
    '''
        register_details = {
                            email: email
                            password:password
                            fname: f_name
                            lname: l_name
                            location: location
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
    user.location = signUpDetails.get("location")

    db.session.add(user)
    db.session.commit()

    return jsonify(user.to_json()), 201
