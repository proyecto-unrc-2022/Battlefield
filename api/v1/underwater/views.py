from api import token_auth

from . import underwater
from app.daos.underwater.uw_game_dao import create_game

@underwater.get('/new_game')
# @token_auth.login_required
def new_game():
    ng = create_game()
    return ng.__repr__()