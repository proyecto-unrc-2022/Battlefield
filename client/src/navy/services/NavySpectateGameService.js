import axios from "axios";
import authHeader from "../../services/auth-header";

const API_URL = "http://127.0.0.1:5000/api/v1/navy";


class NavySpectateGameService {
    getNavySpectateGames(navy_game_id,round) {
        return axios.get(API_URL + "/spectate/" + navy_game_id + "/" + round, {
            headers: authHeader(),
        });
    }
    }

export default new NavySpectateGameService();