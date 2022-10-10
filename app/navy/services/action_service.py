from app.navy.validators.action_request_validator import ActionRequestValidator
class ActionService:

    def validate_action(request):
       return ActionRequestValidator().load(request)




