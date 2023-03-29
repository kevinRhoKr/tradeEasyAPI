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
    reported = db.Column(db.Integer)

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


class Item(db.Model):
    __tablename__ = "item"
    item_id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(320))
    name = db.Column(db.String(30))
    description = db.Column(db.String(200))
    location = db.Column(db.String(64))
    reported = db.Column(db.Integer)

    @staticmethod
    def from_json(json_item):
        item_id = json_item.get("item_id")
        email = json_item.get("email")
        name = json_item.get("name")
        description = json_item.get("description")
        location = json_item.get("location")
        if item_id is None:
            raise ValueError("Item doesn't have an ID")
        return Item(item_id=item_id, email=email, name=name, description=description, location=location, reported=0)

    def to_json(self):
        json_item = {
            "item_id": self.item_id,
            "email": self.email,
            "name": self.name,
            "description": self.description,
            "location": self.location,
        }
        return json_item


class Conversation(db.Model):
    __tablename__ = "conversation"
    chat_id = db.Column(db.Integer, primary_key=True)
    email1 = db.Column(db.String(320))
    email2 = db.Column(db.String(320))
    item_id = db.Column(db.Integer)

    def to_json(self):
        json_conversation = {
            "chat_id": self.chat_id,
            "email1": self.email1,
            "email2": self.email2,
            "item_id": self.item_id,
        }

        return json_conversation

    @staticmethod
    def from_json(json_conv):
        chat_id = json_conv.get("chat_id")
        email1 = json_conv.get("email1")
        email2 = json_conv.get("email2")
        item_id = json_conv.get("item_id")
        if chat_id is None:
            raise ValueError("Conversation does not have an ID")
        return Item(chat_id=chat_id, email1=email1, email2=email2, item_id=item_id)


class Likes(db.Model):
    __tablename__ = "likes"
    email = db.Column(db.String(320), primary_key=True)
    item_id = db.Column(db.Integer, primary_key=True)

    def to_json(self):
        json_conversation = {
            "email": self.email,
            "item_id": self.item_id,
        }

        return json_conversation

    @staticmethod
    def from_json(json_conv):
        email = json_conv.get("email")
        item_id = json_conv.get("item_id")
        if email is None or item_id is None:
            raise ValueError("Cannot get the interest information")
        return Item(email=email, item_id=item_id)
