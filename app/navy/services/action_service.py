from app.navy.daos.action_dao import action_dao
from app.navy.models.action import Action
from app.navy.validators.action_request_validator import ActionRequestValidator


class ActionService:
    def validate_request(self, request):
        return ActionRequestValidator().load(request)

    def add(self, action):
        action_dao.add_or_update(Action(**action))


action_service = ActionService()
