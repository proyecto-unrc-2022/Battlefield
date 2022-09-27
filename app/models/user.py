from marshmallow_sqlalchemy import SQLAlchemyAutoSchema, SQLAlchemySchema, auto_field
from marshmallow_sqlalchemy.fields import Nested
from sqlalchemy.orm import relationship

from app import db


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(100), unique=False, nullable=False)

    profile = relationship("Profile", uselist=False, back_populates="user")

    def __init__(self, username=None, email=None, password=None):
        self.username = username
        self.email = email
        self.password = password

    def __repr__(self):
        return "<User %r>" % self.username


class Profile(db.Model):
    __tablename__ = "profile"

    id = db.Column(db.Integer, primary_key=True)
    dob = db.Column(db.DateTime)
    job = db.Column(db.String(100))

    user_id = db.Column(db.Integer, db.ForeignKey(User.id))

    user = relationship("User", back_populates="profile")


class ProfileSchema(SQLAlchemyAutoSchema):
    class Meta:
        model = Profile
        include_relationships = True
        load_instance = True


class UserSchema(SQLAlchemySchema):
    class Meta:
        model = User
        include_relationships = True
        load_instance = True

    id = auto_field()
    username = auto_field()
    email = auto_field()
    profile = Nested(ProfileSchema, many=False, exclude=("user",))
