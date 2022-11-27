import axios from "axios";
import authHeader from "../../services/auth-header";

const API_URL = "http://127.0.0.1:5000/api/v1/navy/navy_games";

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

  postNavyGame(){
    return axios.post(API_URL, {},{
      headers: authHeader(),
    });
  }

  patchNavyGame(id){
    return axios.patch(API_URL + `/${id}`,{},{
      headers: authHeader(),
    });
  }

  deleteNavyGame(id){
    return axios.delete(API_URL + `/${id}`,{
      headers: authHeader(),
    });
  }


}

export default new NavyGameService();
