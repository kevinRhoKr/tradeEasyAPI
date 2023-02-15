import os
from app import create_app, db

app = create_app(os.getenv("FLASK_CONFIG") or "default")


def create_database():
    db.create_all()

if __name__ == "__main__":
    #create_database()
    app.run('127.0.0.1', port=5000, debug=True)