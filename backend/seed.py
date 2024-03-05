from models import db

def seed_db() :
    db.create_all()
    db.session.commit()

