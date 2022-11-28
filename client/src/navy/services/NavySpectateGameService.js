import axios from "axios";
import authHeader from "../../services/auth-header";
import { API_URL as url } from "../API_URL";

const API_URL = `${url}/api/v1/navy`;

class NavySpectateGameService {
  getNavySpectateGames(navy_game_id, round = 0) {

    return axios.get(API_URL + "/spectate/" + navy_game_id, {
      params: {
        round: round,
      },
      headers: authHeader(),
    });
  }
}

export default new NavySpectateGameService();
