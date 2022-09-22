import json

from marshmallow_sqlalchemy import SQLAlchemyAutoSchema, auto_field
from marshmallow_sqlalchemy.fields import Nested
from sqlalchemy.orm import relationship

from app import db
from app.models.user import User


class UnderGame(db.Model):
    __tablename__ = "under_games"
    id = db.Column(db.Integer, primary_key=True)

    host_id = db.Column(db.Integer, db.ForeignKey(User.id))
    visitor_id = db.Column(db.Integer, db.ForeignKey(User.id))

    # host = relationship("User", uselist=False, foreign_keys="user.id")
    # visitor = relationship("User", uselist=False, foreign_keys="user.id")

    def __repr__(self):
        return json.dumps(
            {"game_id": self.id, "host_id": self.host_id, "visitor_id": self.visitor_id}
        )


class UnderGameSchema(SQLAlchemyAutoSchema):
    class Meta:
        model = UnderGame
        include_relationships = True
        load_instance = True

    id = auto_field()
    host_id = auto_field()
    visitor_id = auto_field()
