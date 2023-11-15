from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt

bcrypt = Bcrypt()
db = SQLAlchemy()


def connect_db(app):
    """Connect to database."""

    app.app_context().push()
    db.app = app
    db.init_app(app)


class User(db.Model):
    """User model"""

    __tablename__ = "users"

    username = db.Column(
        db.String(30),
        primary_key=True,
    )

    first_name = db.Column(
        db.String(30),
        nullable=False,
    )

    last_name = db.Column(
        db.String(30),
        nullable=False,
    )

    email = db.Column(
        db.String(50),
        nullable=False,
        unique=True,
    )

    password = db.Column(
        db.String(120),
        nullable=False,
    )

    created_at = db.Column(
        db.DateTime,
        default=db.func.now(),
        nullable=False,
    )

    isAdmin = db.Column(
        db.Boolean,
        default=False,
        nullable=False,
    )

    listings = db.relationship(
        "Space",
        secondary="users_spaces",
        backref="owner",
    )

    @classmethod
    def signup(cls, username, first_name, last_name, email, password):
        """Sign up user.

        Hashes password and adds user to db
        """
        hashed_pwd = bcrypt.generate_password_hash(password).decode("UTF-8")

        user = User(
            username=username,
            first_name=first_name,
            last_name=last_name,
            email=email,
            password=hashed_pwd,
        )

        db.session.add(user)
        return user

    @classmethod
    def authenticate(cls, username, password):
        """Find user with `username` and `password`.

        This is a class method (call it on the class, not an individual user.)
        It searches for a user whose password hash matches this password
        and, if it finds such a user, returns that user object.

        If this can't find matching user (or if password is wrong), returns
        False.
        """
        user = cls.query.filter_by(username=username).one_or_none()

        if user:
            is_auth = bcrypt.check_password_hash(user.password, password)
            if is_auth:
                return user

        return False


class Space(db.Model):
    """Space model"""

    __tablename__ = "spaces"

    id = db.Column(
        db.Integer,
        primary_key=True,
    )

    title = db.Column(
        db.String(40),
        nullable=False,
    )

    description = db.Column(
        db.Text,
        nullable=True,
    )

    price = db.Column(
        db.Numeric(2),
        nullable=False,
    )

    address = db.Column(
        db.String(120),
        nullable=False,
        unique=True,
    )

    listed_at = db.Column(
        db.DateTime,
        default=db.func.now(),
        nullable=False,
    )

    last_booked = db.Column(
        db.DateTime,
        nullable=True,
    )

    images = db.relationship("Image", backref="listing")


class User_Space(db.Model):
    """User Spaces Thru table"""

    __tablename__ = "users_spaces"

    username = db.Column(
        db.String(30),
        db.ForeignKey("users.username"),
        primary_key=True,
        nullable=False,
    )

    space_id = db.Column(
        db.Integer,
        db.ForeignKey("spaces.id"),
        primary_key=True,
        nullable=False,
    )


class Image(db.Model):
    """Image model"""

    __tablename__ = "images"

    id = db.Column(
        db.Integer,
        primary_key=True,
    )

    space_id = db.Column(
        db.Integer,
        db.ForeignKey("spaces.id"),
        nullable=False,
    )

    url = db.Column(
        db.String(200),
        nullable=False,
    )


class Booking(db.Model):
    """Booking model"""

    __tablename__ = "bookings"

    id = db.Column(
        db.Integer,
        primary_key=True,
    )

    username = db.Column(
        db.String(30),
        db.ForeignKey("users.username"),
        nullable=False,
    )

    space_id = db.Column(
        db.Integer,
        db.ForeignKey("spaces.id"),
        nullable=False,
    )

    price = db.Column(
        db.Numeric(2),
        nullable=False,
    )

    check_in = db.Column(
        db.Date,
        nullable=False,
    )

    check_out = db.Column(
        db.Date,
        nullable=True,
    )

    created_at = db.Column(
        db.DateTime,
        default=db.func.now(),
        nullable=False,
    )

    space = db.relationship("Space", backref="booking")
    renter = db.relationship("User", backref="booking")
