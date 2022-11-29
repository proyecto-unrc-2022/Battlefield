import axios from "axios";
import authHeader from "../../services/auth-header";
import { API_URL as url } from "../API_URL";

const API_URL = `${url}/api/v1/navy`;

class ActionService {
  sendAction(action) {
    return axios.post(
      API_URL + "/actions",
      { ...action },
      {
        headers: authHeader(),
      }
    );
  }
}

export default new ActionService();
