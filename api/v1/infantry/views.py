import json
from api import token_auth

from app import db

from flask import Response, jsonify, request

from app.daos.infantry.infantry_dao import add_figure
from app.daos.infantry.infantry_dao import create_game
from app.daos.infantry.infantry_dao import ready
from app.daos.infantry.infantry_dao import join
from app.daos.infantry.infantry_dao import move_by_user
from app.daos.infantry.infantry_dao import shoot
from app.models.infantry.infantry_game import Game_Infantry, Figure_infantry, Game_Infantry_Schema, Projectile_Infantry_Schema, Figure_Infantry_Schema, Projectile
from . import infantry

game_schema= Game_Infantry_Schema()
figure_schema = Figure_Infantry_Schema()
projectile_schema = Projectile_Infantry_Schema()

#figure = db.session.query(Figure_infantry).where(Figure_infantry.id_user == user_id and Figure_infantry.id_game == game_id).one_or_none()


@infantry.route("/create_game/user/<user_id>",methods=['POST'])
def start_game(user_id):

    if(create_game(user_id) == None):
        return Response(status=404)
    
    new_game = Game_Infantry.query.filter_by(id_user1 = user_id).first()

    return jsonify(game_schema.dump(new_game))
    

@infantry.route("/ready_to_play/game/<game_id>",methods=['POST'])
def ready_to_play(game_id):

    if (ready(game_id)):
        
        id_game = db.session.query(Game_Infantry).where(Game_Infantry.id == game_id).one_or_none()

        return jsonify(game_schema.dump(id_game))

    else:
        return Response(status=404)

    

@infantry.route("/join_game/game/<game_id>/user/<user_id>",methods=['POST'])
def join_game(game_id, user_id):

    if (join(game_id, user_id)):

        ready_game = Game_Infantry.query.filter_by(id = game_id, id_user2 = user_id).first()

        return jsonify(game_schema.dump(ready_game))

    
    return Response(status=404)



@infantry.route("/create_entity/game/<game_id>/user/<user_id>/figure/<figure_id>",methods=['POST'])
def choose_figure(game_id, user_id ,figure_id):
    if (not(add_figure(game_id, user_id ,figure_id))):
        
        return Response(status=404)

    entity = Figure_infantry.query.filter_by(id_game = game_id, id_user = user_id).first()

    return jsonify(figure_schema.dump(entity))
        

#revisar la logica de moverse 
@infantry.route("/move/game/<game_id>/user/<user_id>/course/<direction>/velocity/<velocity>",methods=['POST'])
def mov_action(direction, velocity, user_id, game_id):
    if(move_by_user(game_id, user_id, direction, velocity)):
        
        move_entity = db.session.query(Figure_infantry).where(Figure_infantry.id == game_id and Figure_infantry.id_user == user_id).one_or_none()
        
        return jsonify(figure_schema.dump(move_entity))
    
    return Response(status=404)

@infantry.route("/shoot/game/<game_id>/course/<direction>/figure/<figure_id>",methods=['POST'])
def shoot_entity(direction, figure_id, game_id):

    if(shoot(direction, figure_id, game_id)):

        projectile = db.session.query(Projectile).order_by(Projectile.id.desc()).first()

        return jsonify(projectile_schema.dump(projectile))
    else:
        return Response(status=404)


#@infantry.route("/games",methods=['POST'])
#def games_test():
#
#    data = json.loads(request.data)
#    user1_id = data["id_user1"]
#    user2_id = data["id_user2"]
#
#    game = Game_Infantry(id_user1= user1_id, id_user2= user2_id)
#
#    return jsonify(game_schema.dump(game))

    




    
# Routes here
