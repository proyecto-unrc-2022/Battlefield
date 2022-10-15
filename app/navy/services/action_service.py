from app.navy.daos.action_dao import action_dao
from app.navy.models.action import Action
from app.navy.services.navy_game_service import navy_game_service
from app.navy.services.ship_service import ship_service
from app.navy.validators.action_request_validator import ActionRequestValidator


class ActionService:
    def validate_request(self, request):
        return ActionRequestValidator().load(request)

    def add(self, action:Action):
        action_dao.add_or_update(Action(**action))

    def check_update(self,navy_game_id):
        # TODO: traerte de la bd las acciones de la partida, y si hay 2, actualizar el estado de la partida
        actions = action_dao.get_by(navy_game_id=navy_game_id)
        if len(actions) == 2:
            navy_game_service.update_game(navy_game_id)

    def delete(self,action):
        action_dao.delete(action)
    
    def get_by_user(self, user_id, navy_game_id):
        return action_dao.get_by_user(user_id,navy_game_id)

    def execute(self,action):
        ship = ship_service.get_by_id(action.ship_id)
        ship.course = action.course
        if ship_service.turn(ship):
            if action.attack:
                return ship_service.attack(ship)
            return ship_service.move(ship, action)
        else:
            return False

            
        

action_service = ActionService()
