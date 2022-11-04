from app.navy.daos.action_dao import action_dao
from app.navy.models.action import Action
from app.navy.services.ship_service import ship_service
from app.navy.validators.action_request_validator import ActionRequestValidator

""" 
    ActionService is responsible for handling all the business logic related to the actions game.
    It is responsible for validating the actions, and executing them.

    Note: This service is not responsible for the movement of the missiles, that logic is handled by the NavyGameService.
 """


class ActionService:
    actions = {1: ship_service.attack, 0: ship_service.update_position}

    def validate_request(self, request):
        return ActionRequestValidator().load(request)

    def add(self, action: Action):
        action_dao.add_or_update(Action(**action))

    def get_by_round(self, navy_game_id, round, turn):
        actions = action_dao.get_by_round(navy_game_id, round)
        actions.sort(key=lambda x: x.user_id == turn, reverse=True)
        return actions

    def can_execute(self, ship):
        return ship_service.can_update(ship)

    def execute(self, action):
        from app.navy.services.navy_game_service import navy_game_service
        from app.navy.services.ship_service import ship_service

        ship = navy_game_service.get_ship_from_game(action.navy_game_id, action.ship_id)
        if ship_service.turn(ship, action.course):
            self.actions[action.attack](ship, action)


action_service = ActionService()