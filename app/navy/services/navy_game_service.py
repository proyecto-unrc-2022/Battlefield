from app.navy.validators.navy_game_request_validator import NavyGameRequestValidator
from app.navy.daos.navy_game_dao import navy_game_dao

class NavyGameService: 

  def add(request):
    navy_game_request_validator = NavyGameRequestValidator()
    navy_game = navy_game_request_validator.dump(request)
    navy_game_dao.add_or_update(navy_game)
    return navy_game

navy_game_service = NavyGameService()
