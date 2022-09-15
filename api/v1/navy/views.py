from api import token_auth 
from flask import jsonify
from . import navy
from app.navy.game import Game

@navy.get("/play")
def play():
  return jsonify(Game.read_data("app/navy/start.json"))