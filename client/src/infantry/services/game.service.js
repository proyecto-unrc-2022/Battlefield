import axios from "axios";
import authHeader from "../../services/auth-header";


const API_URL = "http://127.0.0.1:5000/api/v1/infantry"

class GameService {

    getGames(){
        return axios.get(API_URL + "/games", {headers : authHeader()});

    }

    createGame(id){
        return axios.post(API_URL + `/user/${id}/game`,{} , {headers : authHeader()});
    }

    joinGame(id_game, id_user){
        return axios.post(API_URL + `/game/${id_game}/user/${id_user}/join`,{} , {headers : authHeader()});

    }

    ready(id_game){
        

        return axios.post(API_URL + "/game", {"game_id" : id_game}, {headers : authHeader()});

    }

    choose_figure(id_game, id_user, type_figure, posX, posY){


        return axios.post(API_URL + `/game/${id_game}/user/${id_user}/figure/${type_figure}/create_entity`, 
        {
            "pos_x": posX,
            "pos_y": posY
        }, 
        {headers : authHeader()});
    }

    character_wait(id_game, id_user){

        return axios.post(API_URL + "/ready_to_play", 
        { 
            "game_id" : id_game,
            "user_id" : id_user
        },
        {headers : authHeader()});

    }


}

export default new GameService();