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


}

export default new GameService();