import axios from "axios";
import authHeader from "./auth-header";

const API_URL = "http://127.0.0.1:5000/api/users";

class UserService {
  getPublicContent() {
    return axios.get(API_URL + "", {
      headers: { "Content-Type": "application/json" },
    });
  }

  getUserBoard(id) {
    return axios.get(API_URL + `/${id}`, { headers: authHeader() });
  }

  getModeratorBoard() {
    return axios.get(API_URL + "mod", { headers: authHeader() });
  }

  getAdminBoard() {
    return axios.get(API_URL + "admin", { headers: authHeader() });
  }
}

export default new UserService();
