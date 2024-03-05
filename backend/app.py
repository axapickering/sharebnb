from flask import Flask, request, jsonify
from datetime import timedelta
import os
import uuid
import boto3
from flask_cors import CORS, cross_origin
from dotenv import load_dotenv
from models import db, connect_db, User, Space, Booking
from sqlalchemy.exc import IntegrityError
from flask_jwt_extended import (
    create_access_token,
    get_jwt_identity,
    jwt_required,
    JWTManager,
)
from seed import seed_db


app = Flask(__name__)
CORS(app)
jwt = JWTManager(app)
load_dotenv()

BUCKET_REGION = os.environ.get("BUCKET_REGION")
BUCKET_NAME = os.environ.get("BUCKET_NAME")
BUCKET_BASE_URL = f"https://{BUCKET_NAME}.s3.{BUCKET_REGION}.amazonaws.com"
AWS_ACCESS_KEY = os.environ.get("AWS_ACCESS_KEY")
AWS_SECRET_KEY = os.environ.get("AWS_SECRET_KEY")

app.config["SQLALCHEMY_ECHO"] = True
app.config["SQLALCHEMY_DATABASE_URI"] = os.environ.get(
    "DATABASE_URL", "postgresql:///sharebnb"
)
app.config["CORS_HEADERS"] = "Content-Type"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

app.config["SECRET_KEY"] = os.environ["SECRET_KEY"]
app.config["JWT_ACCESS_TOKEN_EXPIRES"] = timedelta(hours=1)
app.config["JWT_SECRET_KEY"] = os.environ["JWT_SECRET_KEY"]

connect_db(app)
seed_db()

BOTO3 = boto3.client(
    "s3", aws_access_key_id=AWS_ACCESS_KEY, aws_secret_access_key=AWS_SECRET_KEY
)
s3 = boto3.resource("s3")
bucket = s3.Bucket(BUCKET_NAME)


########################## AUTHENTICATION ##############################


@app.post("/signup")
@cross_origin()
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
@cross_origin()
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


########################### USER ROUTES ################################


@app.get("/users")
@cross_origin()
def get_all_users():
    """Gets a list of all users"""
    users = User.query.all()
    serialized = [user.serialize(showListing=False) for user in users]
    return jsonify({"users": serialized})


@app.get("/users/<username>")
@cross_origin()
def get_user(username):
    """Get data on one user"""
    user = User.query.get_or_404(username)
    return (jsonify(user.serialize(showBookings=True)), 200)


@app.route("/users/<username>", methods=["PATCH"])
@jwt_required()
@cross_origin()
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
        userReturn = User.query.get_or_404(tokenData["username"])
        return (jsonify(userReturn.serialize()), 200)
    except IntegrityError:
        return (jsonify({"Error": "Invalid body"}), 400)


@app.delete("/users/<username>")
@jwt_required()
@cross_origin()
def delete_user(username):
    """Deletes a user and their info"""
    user = get_jwt_identity()

    if user["username"] != username and user["isAdmin"] is False:
        return (jsonify({"Error": "Unauthorized deletion"}), 401)

    try:
        user = User.query.get_or_404(username)
        db.session.delete(user)
        db.session.commit()
    except:
        return (jsonify({"Error": "Deletion failed"}), 400)

    return (jsonify("Successful deletion"), 200)


########################### SPACE ROUTES ###############################


@app.get("/spaces")
@cross_origin()
def get_all_spaces():
    """Gets a list of all spaces, optionally filtering on nameLike arg"""

    query = request.args.get("nameLike")
    spaces = (
        Space.query.filter(Space.title.ilike(f"%{query}%"))
        if query
        else Space.query.all()
    )
    serialized = [space.serialize() for space in spaces]
    return (jsonify({"spaces": serialized}), 200)


@app.get("/spaces/<int:id>")
@cross_origin()
def get_space(id):
    """Get data on one space by id"""
    space = Space.query.get_or_404(id)
    return (jsonify(space.serialize(showBookings=True)), 200)


@app.post("/spaces")
@cross_origin()
@jwt_required()
def create_listing():
    """Creates a new space"""

    data = request.form

    user = get_jwt_identity()
    random_uuid = str(uuid.uuid4())
    image = request.files.get("image")


    try:
        bucket.upload_fileobj(
            Fileobj=image,
            Key=random_uuid,
            ExtraArgs={"ContentType": f"{image.content_type}"},
        )

        url = f"https://{BUCKET_NAME}.s3.amazonaws.com/{random_uuid}"
        space = Space(**data, image_url=url)
        user = User.query.get_or_404(user['username'])
        user.listings.append(space)
        db.session.add(space)
        db.session.commit()

    except IntegrityError:
        return (jsonify({"Error": "Invalid Request"}), 400)
    except ValueError:
        return (jsonify({"Error": "Missing Required Field"}), 400)

    return (jsonify(space.serialize()), 201)


@app.route("/spaces/<int:id>", methods=["PATCH"])
@cross_origin()
@jwt_required()
def update_space(id):
    """Updates one space's info"""
    data = request.json
    tokenData = get_jwt_identity()
    space = Space.query.get_or_404(id)

    if tokenData["username"] != space.owner.username and tokenData["isAdmin"] is False:
        return (jsonify({"Error": "Unauthorized edit"}), 401)

    if id in data:
        return (jsonify({"Error": "ID is uneditable."}), 400)

    try:
        space.edit_space(**data)
        db.session.commit()
        return (jsonify("Space edited successfully"), 200)
    except:
        return (jsonify({"Error": "Invalid body"}), 400)


@app.delete("/spaces/<int:id>")
@cross_origin()
@jwt_required()
def delete_space(id):
    """Deletes a space"""

    tokenData = get_jwt_identity()
    space = Space.query.get_or_404(id)

    if tokenData["username"] != space.owner.username and tokenData["isAdmin"] is False:
        return (jsonify({"Error": "Unauthorized deletion"}), 401)

    try:
        db.session.delete(space)
        db.session.commit()
    except:
        return (jsonify({"Error": "Deletion failed"}), 400)

    return (jsonify("Successful deletion"), 200)


######################## BOOKING ROUTES ###############################


@app.get("/bookings")
@cross_origin()
def get_all_bookings():
    """Gets a list of all bookings"""
    bookings = Booking.query.all()
    serialized = [booking.serialize() for booking in bookings]
    return (jsonify({"bookings": serialized}), 200)


@app.get("/bookings/<int:id>")
@cross_origin()
def get_booking(id):
    """Get data on one booking"""
    booking = Booking.query.get_or_404(id)
    return (jsonify(booking.serialize()), 200)


@app.post("/bookings")
@cross_origin()
@jwt_required()
def create_booking():
    """Create a new booking"""
    tokenData = get_jwt_identity()
    data = request.json

    try:
        booking = Booking(**data, username=tokenData["username"])
        # user = User.query.get_or_404(tokenData['username'])
        # booking.renter = user
        db.session.add(booking)
        db.session.commit()

    except ValueError:
        return (jsonify({"Error": "Missing Required Field"}), 400)

    except:
        return (jsonify({"Error": "Invalid Request"}), 400)

    return (jsonify({"booking": booking.serialize()}), 201)


@app.route("/bookings/<int:id>", methods=["PATCH"])
@cross_origin()
@jwt_required()
def update_booking(id):
    """Updates one booking's info"""
    data = request.json
    tokenData = get_jwt_identity()
    booking = Booking.query.get_or_404(id)

    if (
        tokenData["username"] != booking.renter.username
        and tokenData["isAdmin"] is False
    ):
        return (jsonify({"Error": "Unauthorized edit"}), 401)

    if "id" in data:
        return (jsonify({"Error": "ID is uneditable."}), 400)
    if "space_id" in data:
        return (jsonify({"Error": "space_id is uneditable."}), 400)
    if "username" in data:
        return (jsonify({"Error": "username is uneditable."}), 400)

    try:
        booking.edit_booking(**data)
        db.session.commit()
        return (jsonify("Booking edited successfully"), 200)
    except:
        return (jsonify({"Error": "Invalid body"}), 400)


@app.delete("/bookings/<int:id>")
@cross_origin()
@jwt_required()
def delete_booking(id):
    """Deletes a booking"""

    tokenData = get_jwt_identity()
    booking = Booking.query.get_or_404(id)

    if (
        tokenData["username"] != booking.renter.username
        or tokenData["username"] != booking.space.owner.username
    ) and tokenData["isAdmin"] is False:
        return (jsonify({"Error": "Unauthorized deletion"}), 401)

    try:
        db.session.delete(booking)
        db.session.commit()
    except:
        return (jsonify({"Error": "Deletion failed"}), 400)

    return (jsonify("Successful deletion"), 200)
