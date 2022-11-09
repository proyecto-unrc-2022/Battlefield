import axios from "axios";
import { json } from "react-router-dom";

const API_URL = "http://127.0.0.1:5000/api/v1/air_force/";

class AirForceService {
    createAirforceGame(){
      return axios
        .post(
          API_URL + "new_game/player/1",
          {
            headers: {
              "Content-Type": "application/json",
            },
          }
        )
      }

    joinAirforceGame(){
      return axios
        //pasarle el id del juego creado sino tira un 400 bad request, no encuentra el game 
        .put(
          API_URL + `join/game/1/player/1`,
          {
            headers: {
              "Content-Type": "application/json",
            }
          }
        ).then ((response) => {
          return response.data;
        });
    }
}
export default new AirForceService();