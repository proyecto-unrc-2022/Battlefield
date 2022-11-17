import axios from "axios";
import AuthService from "../../services/auth.service";

const API_URL = "http://127.0.0.1:5000/api/v1/infantry/";
class InfantryService{

    async getFigure(user_id, game_id){
    let data = {game_id: game_id, user_id, user_id}
    return await axios.post(
        API_URL + "figure", 
            data,
        {
            headers: {
                "Content-Type": "application/json",
                },
        }
    ).then((response) => {
        return response.data;
        });
    }
    async getProjectile(game_id){
        let data = {game_id: game_id}
        return await axios.post(
            API_URL + "projectiles",
            data,
            {
                headers:{
                    "Content-Type": "application/json",
                },
            }
        ).then((response) =>{
            return response.data
        });
    }

    async getUsers(game_id){
        let data = {game_id: game_id}
        return await axios.post(
            API_URL + "game",
            data,
            {
                headers:{
                    "Content-Type": "application/json",
                },
            }
        ).then((response) =>{
            console.log(response.data)
            return response.data
        })
    }
}

export default new InfantryService();
