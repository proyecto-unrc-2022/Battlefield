from app.navy.validators.actionRequestValidator import ActionRequestValidator
class ActionService:

    def validate_action(request):
       return ActionRequestValidator().load(request)




