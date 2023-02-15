from flask import jsonify
from ..models import User
from . import auth


@auth.route('/')
def hello():
    return jsonify({"Hello World!": 1})


@auth.route('/getAll')
def getAll():
    users = User.query.all()
    response = jsonify({"Users": [user.to_json() for user in users]})
    return response

#
# @auth.route("/login", methods=["POST", "GET"])
# def login():
#
#     return render_template('auth/login.html', form=form)