from app.navy.validators.navy_game_request_validator import NavyGameRequestValidator
from app.navy.daos.navy_game_dao import navy_game_dao
from app.navy.models.navy_game import NavyGame

class NavyGameService: 

  def add(request):
    navy_game_request_validator = NavyGameRequestValidator()
    validated_navy_game = navy_game_request_validator.load(request)
    navy_game = NavyGame(10, 20, validated_navy_game["user1_id"])
    navy_game_dao.add_or_update(navy_game)
    return navy_game

navy_game_service = NavyGameService()
