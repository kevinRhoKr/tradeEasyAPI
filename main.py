import os
from app import create_app, db
# from flask_mail import Mail

app = create_app("production")


def create_database():
    db.create_all()

if __name__ == "__main__":
    #create_database()
    # mail = Mail(app)
    app.run()
