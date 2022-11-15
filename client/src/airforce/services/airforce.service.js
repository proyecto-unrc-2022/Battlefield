import axios from "axios";
import { json } from "react-router-dom";
import AuthService from "../../services/auth.service";
import authHeader from "../../services/auth-header";
const API_URL = "http://127.0.0.1:5000/api/v1/air_force/";


class AirForceService {
    createAirforceGame(){
      return axios.post(
          API_URL + "new_game",{},
          {
            headers: authHeader()
          }
        ).then((response) => {
          return response;
        });
      }

    joinAirforceGame(gameId){
      console.log(gameId);
      return axios
        //pasarle el id del juego creado sino tira un 400 bad request, no encuentra el game 
        .put(
          API_URL + `join/game/${gameId}`,{},
          {
            headers: authHeader()
          }
        ).then ((response) => {
          return response;
        });
    }

    choosePlaneAndPosition(plane, course, x, y){
      // const header = {
      //   'Content-Type': 'application/json',
      //   'Authorization': authHeader(),
      // }
      return axios
        .put(
          API_URL + "choose_plane",
          {
            plane,
            course,
            x,
            y,
          },
          {
            headers: authHeader(),       
          }
        ).then((response) => {
          return response
        })
    }
}
export default new AirForceService();