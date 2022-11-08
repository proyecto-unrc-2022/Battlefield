import axios from "axios";
import authHeader from "../../services/auth-header";

const API_URL = "http://127.0.0.1:5000/api/v1/navy";

class ShipService {
  getShipTypes() {
    return axios.get(API_URL + "/ship_types", {
      headers: authHeader(),
    });
  }
}

export default new ShipService();
