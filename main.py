import os
from app import create_app, db

app = create_app("production")

def create_database():
    db.create_all()

if __name__ == "__main__":
    #create_database()
    app.run()