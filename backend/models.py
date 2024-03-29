from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.dialects.postgresql import ExcludeConstraint
from flask_bcrypt import Bcrypt
from psycopg2.extras import DateRange

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

    def serialize(self, showListing=True, showBookings=False):
        """Serialize to dictionary."""
        userDict = {
            "username": self.username,
            "firstName": self.first_name,
            "lastName": self.last_name,
            "email": self.email,
            "isAdmin": self.isAdmin,
        }

        if showListing:
            listings = [listing.serialize(showOwner=False) for listing in self.listings]
            userDict["listings"] = listings

        if showBookings:
            bookings = [bookings.serialize() for bookings in self.bookings]
            userDict["bookings"] = bookings

        return userDict

    def edit_user(self, username=None, email=None, firstName=None, lastName=None):
        """Edits user profile"""

        self.first_name = firstName or self.first_name
        self.last_name = lastName or self.last_name
        self.email = email or self.email


class Space(db.Model):
    """Space model"""

    __tablename__ = "spaces"

    id = db.Column(
        db.Integer,
        primary_key=True,
    )

    owner_user = db.Column(
        db.String(40),
        db.ForeignKey("users.username"),
        nullable=False,
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
        db.Numeric(12, 2),
        nullable=False,
    )

    address = db.Column(
        db.String(120),
        nullable=False,
        unique=False,
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

    image_url = db.Column(db.Text, nullable=True)

    def serialize(self, showOwner=True, showBookings=False):
        """Serialize to dictionary."""

        listingDict = {
            "id": self.id,
            "title": self.title,
            "description": self.description,
            "price": self.price,
            "address": self.address,
            "listedAt": self.listed_at,
            "lastBooked": self.last_booked,
            "imageUrl": self.image_url,
        }

        if showOwner:
            user = self.owner.serialize(showListing=False)
            listingDict["owner"] = user
        if showBookings:
            bookings = Booking.query.filter(Booking.space_id == self.id)
            bookings = [bookings.serialize() for bookings in self.bookings]
            listingDict["bookings"] = bookings
        return listingDict

    def edit_space(
        self,
        id=None,
        title=None,
        description=None,
        price=None,
        address=None,
        listed_at=None,
        lastBooked=None,
    ):
        """Edits users space"""

        self.title = title or self.title
        self.description = description or self.description
        self.price = price or self.price
        self.address = address or self.address
        self.last_booked = lastBooked or self.last_booked


# class Image(db.Model):
#     """Image model"""

#     __tablename__ = "images"

#     id = db.Column(
#         db.Integer,
#         primary_key=True,
#     )

#     space_id = db.Column(
#         db.Integer,
#         db.ForeignKey("spaces.id"),
#         nullable=False,
#     )

#     url = db.Column(
#         db.String(200),
#         nullable=False,
#     )


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
        db.Numeric(12, 2),
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

    space = db.relationship("Space", backref="bookings")
    renter = db.relationship("User", backref="bookings")

    def serialize(self):
        """Serialize to dictionary."""

        return {
            "id": self.id,
            "username": self.username,
            "spaceId": self.space_id,
            "price": self.price,
            "checkIn": self.check_in,
            "checkOut": self.check_out,
            "createdAt": self.created_at,
        }

    def edit_booking(
        self,
        id=None,
        username=None,
        space_id=None,
        price=None,
        checkIn=None,
        checkOut=None,
        created_at=None,
    ):
        """Edits a booking"""

        self.price = price or self.price
        self.check_in = checkIn or self.check_in
        self.check_out = checkOut or self.check_out
