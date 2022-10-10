from app.navy.validators.action_request_validator import ActionRequestValidator
from app.navy.daos.action_dao import action_dao
class ActionService:

    def validate_action(request):
       return ActionRequestValidator().load(request)
    
    def update_action(action):
        action_dao.add_or_update_action(action)





