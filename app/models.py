from werkzeug.security import generate_password_hash, check_password_hash

from . import db
from flask import current_app, url_for
from itsdangerous.url_safe import URLSafeTimedSerializer as Serializer

class User(db.Model):
    __tablename__ = "User"
    email = db.Column(db.String(320), primary_key=True)
    password_hash = db.Column(db.String(128))
    f_name = db.Column(db.String(20))
    l_name = db.Column(db.String(20))
    location = db.Column(db.String(64))

    @staticmethod
    def from_json(json_user):
        f_name = json_user.get("first_name")
        l_name = json_user.get("last_name")
        location = json_user.get("location")
        email = json_user.get("email")
        if f_name is None or f_name == "" or l_name is None or l_name == "":
            raise ValueError("User doesn't have a name")
        return User(f_name=f_name, l_name=l_name, location=location, email=email)

    def to_json(self):
        json_user = {
            "email": self.email,
            "first_name": self.f_name,
            "last_name": self.l_name,
            "location": self.location,
        }
        return json_user

    def __init__(self, **kwargs):
        super(User, self).__init__(**kwargs)

    @property
    def password(self):
        raise AttributeError("password is not a readable attribute")

    @password.setter
    def password(self, password):
        self.password_hash = generate_password_hash(password)

    def verify_password(self, password):
        return check_password_hash(self.password_hash, password)

    def generate_auth_token(self, expiration):
        s = Serializer(current_app.config["SECRET_KEY"], expires_in=expiration)
        return s.dumps({"email": self.email}).decode("utf-8")

    @staticmethod
    def verify_auth_token(token):
        s = Serializer(current_app.config["SECRET_KEY"])
        try:
            data = s.loads(token)
        except:
            return None
        return User.query.get(data["email"])