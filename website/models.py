from . import db
from flask_login import UserMixin
from sqlalchemy.sql import func



class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(150), unique=True)
    password = db.Column(db.String(150))
    first_name = db.Column(db.String(150))
    boards = db.relationship('Board')

class Board(db.Model):
    # __tablename__ = "boards"

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String())
    content = db.Column(db.String())
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    
    # board_image = db.relationship("BoardImage", backref="board", uselist=False)

    def __repr__(self):
        return f"<Board {self.title}>"