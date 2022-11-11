import axios from "axios";
import authHeader from "../../services/auth-header";

const API_URL = "http://127.0.0.1:5000/api/v1/navy";

class ShipService {
  getShipTypes() {
    return axios.get(API_URL + "/ship_types", {
      headers: authHeader(),
    });
  }

  postShip(ship) {
    console.log(ship);
    return axios.post(
      API_URL + "/ships",
      {
        name: ship.name,
        pos_x: ship.pos_x,
        pos_y: ship.pos_y,
        course: ship.course,
        navy_game_id: ship.navy_game_id,
      },
      {
        headers: authHeader(),
      }
    );
  }
}

export default new ShipService();
