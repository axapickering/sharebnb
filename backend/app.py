import os
from flask import Flask, request, jsonify
from dotenv import load_dotenv
from models import db, connect_db, User, Space, Image
from sqlalchemy.exc import IntegrityError
from flask_jwt_extended import (
    create_access_token,
    get_jwt_identity,
    jwt_required,
    JWTManager,
)

app = Flask(__name__)
jwt = JWTManager(app)
load_dotenv()

app.config["SQLALCHEMY_ECHO"] = True
app.config["SQLALCHEMY_DATABASE_URI"] = os.environ.get(
    "DATABASE_URL", "postgresql:///sharebnb"
)
app.config["SECRET_KEY"] = os.environ["SECRET_KEY"]
app.config["JWT_SECRET_KEY"] = os.environ["JWT_SECRET_KEY"]
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

connect_db(app)


@app.post("/signup")
def signup():
    """Signs up user, returning token with user data if successful"""
    data = request.json
    print(data)
    try:
        user = User.signup(
            username=data.get("username"),
            first_name=data.get("firstName"),
            last_name=data.get("lastName"),
            email=data.get("email"),
            password=data.get("password"),
        )
        db.session.commit()

    except IntegrityError:
        return (jsonify({"Error": "Username or email already registered."}), 400)

    access_token = create_access_token(identity=user.serialize())
    return (jsonify(access_token=access_token), 201)


@app.post("/login")
def login():
    """Logs in user, returning token with user data if successful"""
    data = request.json
    user = User.authenticate(username=data.username, password=data.password)
    if user is False:
        return (jsonify({"Error": "Could not authenticate user."}), 400)
    else:
        del user[password]
        access_token = create_access_token(identity=user)
        return (jsonify(access_token=access_token), 201)


@app.get("/users")
def get_all_users():
    """Gets a list of all users"""
    users = User.query.all()
    serialized = [user.serialize() for user in users]
    return jsonify({'users':serialized})


@app.get("/users/<username>")
@jwt_required()
def get_user(username):
    """Get data on one user"""
    user = User.query.get_or_404(username)
    return (jsonify(user.serialize()), 200)


@app.route("/users/<username>", methods=["PATCH"])
@jwt_required()
def update_user(username):
    """Updates one user's info"""
    data = request.json
    tokenData = get_jwt_identity()

    if tokenData.username != username or tokenData.isAdmin is True:
        return (jsonify({"Error": "Unauthorized edit"}), 401)

    user = User.query.get_or_404(tokenData.username)
    user.first_name = data.first_name or user.first_name
    user.last_name = data.last_name or user.last_name
    user.email = data.email or user.email
    try:
        db.session.commit()
        return (jsonify({f"{username} edited successfully"}), 200)
    except IntegrityError:
        return (jsonify({"Error": "Invalid body"}), 400)


@app.delete("/user/<username>")
@jwt_required()
def delete_user(username):
    """Deletes a user and their info"""
    user = get_jwt_identity()

    if user.username != username or user.isAdmin is True:
        return (jsonify({"Error": "Unauthorized deletion"}), 401)

    User.query.get_or_404(username)
    db.session.delete(username)
    db.session.commit()

    return (jsonify({f"{username} delete successfully"}), 200)


@app.get("/spaces")
def get_all_spaces():
    """Gets a list of all spaces"""
    spaces = Space.query.all()
    return (jsonify(spaces),200)


@app.get("/spaces/<int:id>")
@jwt_required()
def get_space(id):
    """Get data on one space"""
    user = User.query.get_or_404(id)
    del user['password']
    return (jsonify({user}), 200)
