
class SpectateService():
    games_spec = {}
    
    def add_round_game(self,game,ships,missiles):
        
       if game.id not in self.games_spec:
              self.games_spec.update({
                game.id: {},
              })

       if game.round not in self.games_spec[game.id]:
            self.games_spec[game.id].update({
                game.round-1: {
                    "ships": ships,
                    "missiles": missiles
                }
            })
  
       print(self.games_spec)

    def get_ships(self,game_id,round):
        ships = self.games_spec[game_id][round]["ships"]
        return ships
 
    def get_missiles(self,game_id,round):
        return self.games_spec[game_id][round]["missiles"]

    def validate_request(self, request):
        from app.navy.validators.spectate_validator import SpectateValidator
        return SpectateValidator().load(request)
    

spectate_service = SpectateService()