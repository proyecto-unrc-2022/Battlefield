import axios from "axios";
import authHeader from "../../services/auth-header";
import { API_URL as url } from "../API_URL";

const API_URL = `${url}/api/v1/navy`;

class ShipService {
  getShipTypes() {
    return axios.get(API_URL + "/ship_types", {
      headers: authHeader(),
    });
  }

  postShip(ship) {
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

  compass = {
    N: { x: -1, y: 0 },
    S: { x: 1, y: 0 },
    E: { x: 0, y: 1 },
    W: { x: 0, y: -1 },
    NE: { x: -1, y: 1 },
    NW: { x: -1, y: -1 },
    SE: { x: 1, y: 1 },
    SW: { x: 1, y: -1 },
  };

  inverseCoords = {
    N: "S",
    S: "N",
    W: "E",
    E: "W",
    SE: "NW",
    NW: "SE",
    SW: "NE",
    NE: "SW",
  };

  outOfRange(row, col) {
    return row < 1 || row > 10 || col < 1 || col > 10;
  }

  buildShip(ship) {
    const positions = [{ x: ship.x, y: ship.y, proa: true }];
    let newRow = ship.x;
    let newCol = ship.y;
    for (let i = 0; i < ship.size - 1; i++) {
      newRow = newRow + this.compass[this.inverseCoords[ship.course]].x;
      newCol = newCol + this.compass[this.inverseCoords[ship.course]].y;
      positions.push({ x: newRow, y: newCol, proa: false });
    }
    return positions;
  }
}

export default new ShipService();
