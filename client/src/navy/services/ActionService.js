import axios from "axios";
import authHeader from "../../services/auth-header";

const API_URL = "http://127.0.0.1:5000/api/v1/navy";

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
