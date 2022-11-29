import axios from "axios";
import authHeader from "../../services/auth-header";
import { API_URL as url } from "../API_URL";

const API_URL = `${url}/api/v1/navy/navy_games`;

class NavyGameService {
  getNavyGames() {
    return axios.get(API_URL + "", {
      headers: authHeader(),
    });
  }

  getNavyGame(id) {
    return axios.get(API_URL + "/" + id, {
      headers: authHeader(),
    });
  }

  postNavyGame() {
    return axios.post(
      API_URL,
      {},
      {
        headers: authHeader(),
      }
    );
  }

  patchNavyGame(id) {
    return axios.patch(
      API_URL + `/${id}`,
      {},
      {
        headers: authHeader(),
      }
    );
  }

  deleteNavyGame(id) {
    return axios.delete(API_URL + `/${id}`, {
      headers: authHeader(),
    });
  }
}

export default new NavyGameService();
