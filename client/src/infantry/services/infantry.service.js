import axios from "axios";


const API_URL = "http://127.0.0.1:5000/api/v1/infantry/";
class InfantryService{

    async getFigure(user_id, game_id){
    let data = {game_id: game_id, user_id: user_id}
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

    getGame(game_id){
        let data = {game_id: game_id}
        return axios.post(
            API_URL + "game",
            data,
            {
                headers:{
                    "Content-Type": "application/json",
                },
            }
        ).then((response) =>{
            return response.data
        })
    }

    async next_turn(game_id){
        let data = {game_id: game_id}
        return await axios.post(
            API_URL + "next_turn",
            data,
            {
                headers:{
                    "Content-Type": "application/json",
                },
            }
        ).then( (response) =>{
            return response.data
        })
    }
    async update_projectiles(game_id){
        let data = {game_id: game_id}
        return await axios.post(
            API_URL + "update_projectiles",
            data,
            {
                headers:{
                    "Content-Type": "application/json",
                },
            }
        ).then((response) =>{
            return response.data
        })
    }
    async update_actions(game_id){
        let data = {game_id: game_id}
        return await axios.post(
            API_URL + "update_user_actions",
            data,
            {
                headers:{
                    "Content-Type": "application/json",
                },
            }
        ).then((response) =>{
            return response.data
        })
    }
    async move(game_id, user_id, course, velocity){
        let data = {game_id: game_id, user_id: user_id, course: course, velocity: velocity}
        return await axios.post(
            API_URL + "move",
            data,
            {
                headers:{
                    "Content-Type": "application/json",
                },
            }
        ).then((response) =>{
            return response.data
        })
    }
    async shoot(game_id, user_id, course){
        let data = {velocity: 0}
        return await axios.post(
            API_URL + "game/" + game_id + "/user/" + user_id + "/direccion/" + course +"/shoot",
            data,
            {
                headers:{
                    "Content-Type": "application/json",
                },
            }
        ).then((response) =>{
            return response.data
        })
    }
}

export default new InfantryService();
