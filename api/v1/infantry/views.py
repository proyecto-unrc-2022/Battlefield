import json
from api import token_auth

from app import db

from flask import Response, jsonify, request

from app.daos.infantry.infantry_dao import add_figure
from app.daos.infantry.infantry_dao import create_game
from app.daos.infantry.infantry_dao import ready
from app.daos.infantry.infantry_dao import join
from app.daos.infantry.infantry_dao import move
from app.daos.infantry.infantry_dao import shoot
from app.daos.infantry.infantry_dao import update_projectile
from app.models.infantry.infantry_game import Game_Infantry, Figure_infantry, Game_Infantry_Schema, Projectile_Infantry_Schema, Figure_Infantry_Schema, Projectile
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
    new_figure = add_figure(game_id, user_id, int(type))
    if(new_figure == None):
        return Response(status=404)
    return jsonify(figure_schema.dump(new_figure))

#revisar la logica de moverse 
@infantry.route("/move",methods=['POST'])
def mov_action():
    data = json.loads(request.data)
    velocity = data["velocity"]
    course = data["course"]
    game_id = data["game_id"]
    user_id = data["user_id"]
    if(move(int(game_id), int(user_id), int(course), int(velocity))):
        move_entity = db.session.query(Figure_infantry).where(Figure_infantry.id == game_id and Figure_infantry.id_user == user_id).one_or_none()
        return jsonify(figure_schema.dump(move_entity))
    return "Colision o velocidad excedida"

@infantry.route("/shoot/game/<game_id>/course/<direction>/figure/<figure_id>",methods=['POST'])
def shoot_entity(direction, figure_id, game_id):
    if(shoot(direction, figure_id, game_id)):

        projectile = db.session.query(Projectile).order_by(Projectile.id.desc()).first()

        return jsonify(projectile_schema.dump(projectile))
    else:
        return Response(status=404)

@infantry.route("/update",methods=['POST'])
def updateProjectile():

    projectile = db.session.query(Projectile).order_by(Projectile.id.desc()).first()
    
    update_projectile(projectile.id)

    return jsonify(projectile_schema.dump(projectile))


    
# Routes here
