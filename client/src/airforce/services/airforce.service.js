import axios from "axios";

const API_URL = "http://127.0.0.1:5000/airforce/";

class AirForceService {
    createAirforceGame(){
        return axios
      .put(
        API_URL + "new_game/player/1",
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
export default new AirForceService();