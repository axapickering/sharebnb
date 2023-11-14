import os
from flask import Flask, request, jsonify
from dotenv import load_dotenv
from models import db, connect_db, User, Space, Image
from sqlalchemy.exc import IntegrityError
from flask_jwt_extended import create_access_token, get_jwt_identity, jwt_required, JWTManager

app = Flask(__name__)

load_dotenv()

app.config["SQLALCHEMY_ECHO"] = True
app.config["SQLALCHEMY_DATABASE_URI"] = os.environ.get(
    "DATABASE_URL", "postgresql:///sharebnb"
)
app.config["DEBUG_TB_INTERCEPT_REDIRECTS"] = False
app.config["SECRET_KEY"] = os.environ["SECRET_KEY"]
app.config["JWT_SECRET_KEY"] = os.environ["JWT_SECRET_KEY"]

app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
jwt = JWTManager(app)

connect_db(app)

@app.post("/signup")
def signup():
    ''' Signs up user, returning token with user data if successful'''
    data = request.json
    try:
        user = User.signup(username=data.username,
                    first_name=data.firstName,
                    last_name=data.lastName,
                    email=data.email,
                    password=data.password)
        db.session.commit()

    except IntegrityError:
        return (jsonify({'Error':'Username or email already registered.'}),400)

    del user[password]
    access_token = create_access_token(identity=user)
    return (jsonify(access_token=access_token),201)

@app.post("/login")
def login():
    ''' Logs in user, returning token with user data if successful '''
    data = request.json
    user = User.authenticate(username=data.username,password=data.password)
    if user is False:
        return (jsonify({'Error':'Could not authenticate user.'}),400)
    else:
        del user[password]
        access_token = create_access_token(identity=user)
        return (jsonify(access_token=access_token),201)



@app.get("/users")
def get_all_users():
    """Gets a list of all users"""
    users = User.query.all()
    return jsonify({users})


@app.get("/user/<username>")
@jwt_required
def get_user(username):
    """Get data on one user"""
    user = User.query.get_or_404(username)
    del user[password]
    return (jsonify({user}),200)

@app.patch("/user/<username>")
@jwt_required
def update_user(username):
    ''' Updates one user's info'''
    data = request.json


@app.delete("/user/<username>")
@jwt_required
def delete_user(username):
    ''' Deletes a user and their info'''
    if (get_jwt_identity().username != username or
        get_jwt_identity().isAdmin is True):
        return (jsonify({"Error":"Unauthorized deletion"}),401)

