import json
from sqlalchemy import insert, select
from api import token_auth

from app import db

from flask import Response, jsonify, request

from app.daos.infantry.infantry_dao import add_figure
from app.daos.infantry.infantry_dao import create_game
from app.daos.infantry.infantry_dao import ready
from app.daos.infantry.infantry_dao import join
from app.daos.infantry.infantry_dao import move_by_user
from app.daos.infantry.infantry_dao import shoot
from app.daos.infantry.infantry_dao import *
from app.models.infantry.game_Infantry import Game_Infantry, Game_Infantry_Schema
from app.models.infantry.figure_infantry import Figure_infantry, Figure_Infantry_Schema
from app.models.infantry.projectile_infantry import Projectile_Infantry_Schema, Projectile
from . import infantry

game_schema= Game_Infantry_Schema()
figure_schema = Figure_Infantry_Schema()
projectile_schema = Projectile_Infantry_Schema()

#figure = db.session.query(Figure_infantry).where(Figure_infantry.id_user == user_id and Figure_infantry.id_game == game_id).one_or_none()


@infantry.route("/user/<user_id>/game", methods=['POST'])
def start_game(user_id):

    new_game = create_game(user_id)

    if(new_game == None):
        return Response(status=404)
    
    return jsonify(game_schema.dump(new_game))
    

@infantry.route("/ready_to_play/game/<game_id>",methods=['POST'])
def ready_to_play(game_id):

    if (ready(game_id)):
        
        id_game = db.session.query(Game_Infantry).where(Game_Infantry.id == game_id).one_or_none()

        return jsonify(game_schema.dump(id_game))

    else:
        return Response(status=404)

    

@infantry.route("/game/<game_id>/user/<user_id>/join",methods=['POST'])
def join_game(game_id, user_id):

    if (join(game_id, user_id)):

        ready_game = Game_Infantry.query.filter_by(id = game_id).first()

        return jsonify(game_schema.dump(ready_game))

    
    return Response(status=404)



@infantry.route("/game/<game_id>/user/<user_id>/figure/<type>/create_entity",methods=['POST'])
def choose_figure(game_id, user_id, type):

    data = json.loads(request.data)

    pos_x = data["pos_x"]
    pos_y = data["pos_y"]

    new_figure = add_figure(game_id, user_id, type, pos_x, pos_y)

    if(new_figure == None):

        return Response(status=404)


    return jsonify(figure_schema.dump(new_figure))

#revisar la logica de moverse 
@infantry.route("/move/game/<game_id>/user/<user_id>/course/<direction>/velocity/<velocity>",methods=['POST'])
def mov_action(direction, velocity, user_id, game_id):
    if(move_by_user(game_id, user_id, direction, velocity)):
        
        move_entity = db.session.query(Figure_infantry).where(Figure_infantry.id == game_id and Figure_infantry.id_user == user_id).one_or_none()
        
        return jsonify(figure_schema.dump(move_entity))
    
    return Response(status=404)

@infantry.route("/game/<game_id>/user/<user_id>/course/<direction>/shoot",methods=['POST'])
def shoot_entity(direction, user_id, game_id):

    if(shoot(direction, user_id, game_id)):

        projectile = db.session.query(Projectile).order_by(Projectile.id.desc()).first()

        return jsonify(projectile_schema.dump(projectile))
    else:
        return Response(status=404)

@infantry.route("/game/<game_id>/update",methods=['POST'])
def updateProjectile(game_id):

    x = getPosition(game_id)   

    #print(x)

    return "ok"

@infantry.route("games", methods=["GET"])
# @token_auth.login_required
def get_all_users():

    games = db.session.scalars(select(Game_Infantry).where(Game_Infantry.id_user2 == None)).all()

    return jsonify(game_schema.dump(games, many=True))

    
# Routes here
