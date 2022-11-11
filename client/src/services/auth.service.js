import axios from "axios";
import jwt_decode from "jwt-decode";

const API_URL = "http://127.0.0.1:5000/auth/";

class AuthService {
  login(username, password) {
    return axios
      .post(
        API_URL + "login",
        {
          username,
          password,
        },
        {
          headers: {
            "Content-Type": "application/json",
          },
        }
      )
      .then((response) => {
        console.log(response);
        if (response.data.token) {
          localStorage.setItem("user", JSON.stringify(response.data));
        }

        return response.data;
      });
  }

  logout() {
    localStorage.removeItem("user");
  }

  getCurrentUser() {
    const user = jwt_decode(JSON.parse(localStorage.getItem("user")).token);
    return user;
  }
}

export default new AuthService();
