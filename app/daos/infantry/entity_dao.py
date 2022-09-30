from app import db
from ...models.user import User

from ...models.infantry.entity import Entity
from ...models.infantry.infantry_game import Game_Infantry

#This method is used for the creating of game
def create_game(user_id):

    game = Game_Infantry(id_user1= user_id, id_user2= None)
    db.session.add(game)
    db.session.commit()
    return db.session.query(Game_Infantry).order_by(Game_Infantry.id.desc()).first().id  

    #if(db.session.query(Game_Infantry).first() != None):
    #    return True
    #else:
    #    return False

#This method is used to choose the order of the players
#def start_of_game(user_id):
    


    #if(db.session.query(Game_Infantry).first().id_user1 == None):
    #    Game_Infantry.id_user1 = user_id
    #elif(db.session.query(Game_Infantry).first().id_user2 == None):
    #    Game_Infantry.id_user2 = user_id       
    
#This method is used to ask if both players are in the game
def ready(game_id):

    if(db.session.query(Game_Infantry).get(1).id_user1 == None or  db.session.query(Game_Infantry).get(1).id_user2 == None):
        return False
    else:
        return True