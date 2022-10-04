from ast import Raise
from marshmallow import fields, Schema,validate, ValidationError, validates, post_load, validates_schema
from app.models.navy.dynamic_game import Game
from app.models.navy.dynamic_ship import DynamicShip
from app.models.user import User
from app.navy.navy_constants import DIRECTIONS, MISSILES_TYPES, SHIP_TYPES
from app.navy.navy_utils import get_move_ship_

class ActionGameRequest(Schema):

    @validates_schema
    def slugify_name(self, in_data):    

       if( in_data.get('attack') == 1 and in_data.get('move') != 0 ):
                raise ValidationError("Movimento invalido")

       if( in_data.get('attack') == 0):
            mov_ship = get_move_ship_(in_data.get('ship_type'))
            
            if( in_data.get('move') > mov_ship):
                raise ValidationError("Cantidad de movimento invalida")

    @validates('id_user')
    def validate_id_user(self, id_user):
        user = User.query.filter_by(id=id_user).first()
        if not user:
            raise ValidationError("El usuario no existe")
   
    @validates('id_game')
    def validate_id_game(self, id_game):
        game = Game.query.filter_by(id=id_game).first()
        if not id_game:
            raise ValidationError("El juego no existe")
    """    
    @validates('id_ship')
    def validate_id_ship(self, id_ship, id_game):
        #ship = DynamicShip.query.filter_by(id=id_ship).first()
        if  id_ship==1 or id_game == 2:
            raise ValidationError("Error id_ship") 
    """

    id_missile = fields.Integer(validate=validate.OneOf(MISSILES_TYPES), required=True)
    id_user = fields.Integer(required=True)
    id_game = fields.Integer(required=True)
    dir = fields.Str(validate=validate.OneOf(DIRECTIONS), required=True)
    id_ship = fields.Int(required=True)
    move = fields.Int(required=True)
    ship_type = fields.Int(validate=validate.OneOf(SHIP_TYPES), required=True)
    attack = fields.Integer(validate=validate.OneOf([0,1]),required=True)
    

   




#validator = validate.And(validate.Range(min=0), is_even)



