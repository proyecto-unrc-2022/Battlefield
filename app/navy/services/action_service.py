from app.navy.daos.action_dao import action_dao
from app.navy.models.action import Action
from app.navy.services.navy_game_service import navy_game_service
from app.navy.services.ship_service import ship_service
from app.navy.validators.action_request_validator import ActionRequestValidator


class ActionService:
    def validate_request(self, request):
        return ActionRequestValidator().load(request)

    def add(self, action: Action):
        action_dao.add_or_update(Action(**action))

    def delete(self, action):
        action_dao.delete(action)

    def get_by_user(self, user_id, navy_game_id):
        return action_dao.get_by_user(user_id, navy_game_id)

    def get_by_navy_game(self, navy_game_id):
        return action_dao.get_by_navy_game_id(navy_game_id)

    def execute(self, action):
        ship = ship_service.get_by_id(action.ship_id)
        if ship_service.turn(ship, action.course):
            if action.attack:
                return ship_service.attack(ship)
            return ship_service.move(ship, action)
        else:
            return False


action_service = ActionService()
