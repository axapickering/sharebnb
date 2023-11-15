from datetime import timedelta
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
from flask.ext.uuid import FlaskUUID

app = Flask(__name__)
jwt = JWTManager(app)
load_dotenv()

BUCKET_REGION = os.environ.get("BUCKET_REGION")
BUCKET_NAME = os.environ.get("BUCKET_NAME")
BUCKET_BASE_URL = f'https://{BUCKET_NAME}.s3.{BUCKET_REGION}.amazonaws.com'

app.config["SQLALCHEMY_ECHO"] = True
app.config["SQLALCHEMY_DATABASE_URI"] = os.environ.get(
    "DATABASE_URL", "postgresql:///sharebnb"
)
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

app.config["SECRET_KEY"] = os.environ["SECRET_KEY"]
app.config["JWT_ACCESS_TOKEN_EXPIRES"] = timedelta(hours=1)
app.config["JWT_SECRET_KEY"] = os.environ["JWT_SECRET_KEY"]

connect_db(app)
FlaskUUID(app)
uuid = FlaskUUID()

import boto3
from botocore.exceptions import ClientError

BOTO3 = boto3.client('s3')


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
        return (jsonify({"Error": "Invalid Request"}), 400)

    except ValueError:
        return (jsonify({"Error": "Missing Required Field"}), 400)

    access_token = create_access_token(identity=user.serialize())
    return (jsonify(access_token=access_token), 201)


@app.post("/login")
def login():
    """Logs in user, returning token with user data if successful"""
    data = request.json
    print("DATA", data)
    user = User.authenticate(username=data["username"], password=data["password"])
    if user is False:
        return (jsonify({"Error": "Could not authenticate user."}), 400)
    else:
        access_token = create_access_token(identity=user.serialize())
        return (jsonify(access_token=access_token), 201)


@app.get("/users")
def get_all_users():
    """Gets a list of all users"""
    users = User.query.all()
    serialized = [user.serialize() for user in users]
    return jsonify({"users": serialized})


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

    if tokenData["username"] != username and tokenData["isAdmin"] is False:
        return (jsonify({"Error": "Unauthorized edit"}), 401)

    if "username" in data:
        return (jsonify({"Error": "Cannot edit username"}), 401)

    if "isAdmin" in data and tokenData["isAdmin"] is False:
        return (jsonify({"Error": "Cannot edit admin status"}), 401)

    user = User.query.get_or_404(tokenData["username"])

    user.edit_user(**data)

    try:
        db.session.commit()
        return (jsonify(f"{username} edited successfully"), 200)
    except IntegrityError:
        return (jsonify({"Error": "Invalid body"}), 400)


@app.delete("/users/<username>")
@jwt_required()
def delete_user(username):
    """Deletes a user and their info"""
    user = get_jwt_identity()

    if user['username'] != username and user['isAdmin'] is False:
        return (jsonify({"Error": "Unauthorized deletion"}), 401)

    try:
        user = User.query.get_or_404(username)
        #Space.query.filter_by(username=user['username']).delete()
        db.session.delete(user)
        db.session.commit()
    except:
        return (jsonify({"Error":"Deletion failed"}),400)

    return (jsonify("Successful deletion"), 200)


@app.get("/spaces")
def get_all_spaces():
    """Gets a list of all spaces"""
    spaces = Space.query.all()
    serialized = [space.serialize() for space in spaces]
    return (jsonify({"spaces":serialized}), 200)


@app.get("/spaces/<int:id>")
@jwt_required()
def get_space(id):
    """Get data on one space"""
    space = Space.query.get_or_404(id)
    return (jsonify(space.serialize()), 200)

@app.post("/spaces")
@jwt_required()
def create_listing():
    ''' Creates a new listing '''
    data = request.form
    for key in request.files:
        image_name = key
    print("Image:",image)
    print("Form:",data)
    user = get_jwt_identity()
    random_uuid = uuid.uuid4()
    try:
        response = BOTO3.put_object(
            Body=request.files.get(image_name),
            Bucket=BUCKET_NAME,
            Key=random_uuid,
        )
        space = Space(**data, image_url=f'random_uuid')
        user = User.query.get_or_404(user['username'])
        space.owner.append(user)
        db.session.commit()
    except IntegrityError:
        return (jsonify({"Error": "Invalid Request"}), 400)
    except ValueError:
        return (jsonify({"Error": "Missing Required Field"}), 400)

    return (jsonify(space.serialize()), 201)