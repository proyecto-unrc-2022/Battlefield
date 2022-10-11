from app.navy.daos.action_dao import action_dao
from app.navy.validators.action_request_validator import ActionRequestValidator
from app.navy.models.action import Action

class ActionService:
    def validate_request(request):
        return ActionRequestValidator().load(request)

    def add(action):
        action_dao.add_or_update(Action(**action))


action_service = ActionService()
