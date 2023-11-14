from flask_sqlalchemy import SQLAlchemy

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

    listings = db.relationship("Space", secondary="users_spaces", backref="owner")


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

    user_id = db.Column(
        db.Integer,
        db.ForeignKey("users.id"),
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
        db.DatTime,
        default=db.func.now(),
        nullable=False,
    )

    space = db.relationship("Space", backref="booking")
    renter = db.relationship("User", backref="booking")
