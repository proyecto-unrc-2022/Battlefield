import axios from "axios";
import authHeader from "../../services/auth-header";
import { API_URL as url } from "../API_URL";

const API_URL = `${url}/api/v1/navy`;

class MissileService {
  getMissileTypes() {
    return axios.get(API_URL + "/missile_types", {
      headers: authHeader(),
    });
  }
}

export default new MissileService();
