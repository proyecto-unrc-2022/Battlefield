from api import token_auth

from . import underwater
from app.underwater.daos.game_dao import create_game

@underwater.get('/new_game')
def new_game():
    ng = create_game()
    return ng.__repr__()