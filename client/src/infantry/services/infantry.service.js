import axios from "axios";
import AuthService from "../../services/auth.service";

const API_URL = "http://127.0.0.1:5000/api/v1/infantry/";
class InfantryService{

    getInfantry(user_id, game_id){
        console.log(user_id)
        let data = {game_id: game_id, user_id, user_id}
        console.log(data)
        return axios.post(
            API_URL + "figure", 
                data,
            {
                headers: {
                    "Content-Type": "application/json",
                  },
            }
        ).then((response) => {
            return response.data;
          });
    }
}

export default new InfantryService();
