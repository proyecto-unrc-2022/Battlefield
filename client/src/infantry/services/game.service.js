import axios from "axios";
import authHeader from "../../services/auth-header";


const API_URL = "http://127.0.0.1:5000/api/v1/infantry"

class GameService {

    getGames(){
        return axios.get(API_URL + "/games", {headers : authHeader()});

    }

    

}

export default new GameService();