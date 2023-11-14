"""Seed database with sample data from CSV Files."""
from app import db
from models import User, Space, Booking, Image

db.drop_all()
db.create_all()

db.session.commit()
