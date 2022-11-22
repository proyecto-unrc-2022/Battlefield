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
      return axios
        .put(
          API_URL + `join/game/${gameId}`,{},
          {
            headers: authHeader()
          }
        );
    }

    airforceGameReady(gameId){
      return axios.get(
          API_URL + `game/${gameId}/ready`,{},
          {
            headers: authHeader()
          }
        )
      }

    choosePlaneAndPosition(plane, course, x, y, id){
      return axios
        .put(
          API_URL + "choose_plane",
          {
            plane,
            course,
            x,
            y,
            id,
          },
          {
            headers: authHeader(),       
          }
        ).then((response) => {
          return response
        })
    }

    getPlanes(){
      return axios
      .get(API_URL + "/get/planes",{},{})
    }
}
export default new AirForceService();