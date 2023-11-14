import os
from flask import Flask, request
from dotenv import load_dotenv
from models import db, connect_db, User, Space, Image

app = Flask(__name__)

app.config["SQLALCHEMY_ECHO"] = True
app.config["SQLALCHEMY_DATABASE_URI"] = os.environ.get(
    "DATABASE_URL", "postgresql:///sharebnb"
)
app.config["DEBUG_TB_INTERCEPT_REDIRECTS"] = False
app.config["SECRET_KEY"] = os.environ["SECRET_KEY"]

app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

connect_db(app)


@app.get("/users")
def get_all_users():
    """Gets a list of all users"""


@app.get("/user/:id")
def get_user():
    """Get data on one user"""
