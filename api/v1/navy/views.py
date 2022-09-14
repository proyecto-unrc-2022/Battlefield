from api import token_auth 

from . import navy

@navy.get("/play")
def play():
  return "Holas"