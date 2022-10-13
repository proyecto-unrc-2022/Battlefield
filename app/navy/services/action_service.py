from app.navy.daos.action_dao import action_dao
from app.navy.models.action import Action
from app.navy.services.navy_game_service import navy_game_service
from app.navy.validators.action_request_validator import ActionRequestValidator


class ActionService:
    def validate_request(request):
        return ActionRequestValidator().load(request)

    def add(action):
        action_dao.add_or_update(Action(**action))

    def check_update(navy_game_id):
        # TODO: traerte de la bd las acciones de la partida, y si hay 2, actualizar el estado de la partida
        actions = action_dao.get_by(navy_game_id=navy_game_id)
        if len(actions) == 2:
            navy_game_service.update_game(navy_game_id)


action_service = ActionService()
