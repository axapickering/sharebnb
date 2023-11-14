from flask_sqlalchemy import SQLAlchemy
import datetime

db = SQLAlchemy()

def connect_db(app):
    """Connect to database."""

    app.app_context().push()
    db.app = app
    db.init_app(app)

class User(db.Model):
    '''User model'''

    __tablename__ = "users"

    username = db.Column(
        db.String(30),
        primary_key=True
    )

    first_name = db.Column(
        db.String(30),
        nullable=False)

    last_name = db.Column(
        db.String(30),
        nullable=False)

    email = db.Column(
        db.String(50),
        nullable=False
    )

    password = db.Column(
        db.String(120),
        nullable=False
    )

class Space(db.Model):
    '''Space model'''

    id = db.Column(
        db.Integer,
        primary_key=True
    )

    title = db.Column(
        db.String(40),
        nullable=False)

    description = db.Column(
        db.Text,
        nullable=True)

    price = db.Column(
        db.Numeric(2),
        nullable=False
    )

    address = db.Column(
        db.String(120),
        nullable=False,
        unique=True
    )

    listed_at = db.Column(
        db.DateTime,
        default=datetime.utcnow,
        nullable=False
    )

    last_booked = db.Column(
        db.DateTime,
        nullable=True
    )


