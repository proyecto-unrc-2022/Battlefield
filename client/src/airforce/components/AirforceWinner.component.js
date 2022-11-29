import React, { Component } from "react";
import userService from "../../services/user.service";
import "./AirforceWinner.css";


export default class AirforceWinner extends Component {
    render(){
        userService.getUserBoard(localStorage.getItem("userWinner")).then(
            (response) => {
                localStorage.setItem("winner", response.data.username)
            }
        )
        const userWinner = localStorage.getItem("winner");
        return(
            <div className="winner">
                <h1>
                Winner: Player {userWinner}!!!
                </h1>
            </div>
        )
    }

}