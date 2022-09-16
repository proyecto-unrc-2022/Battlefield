from flask import jsonify
from app.navy.game import Game
from . import navy


@navy.get("/play")
def play():
  return jsonify(Game.read_data("app/navy/start.json"))
