import React, { Component } from "react";
import "./AirforceWinner.css";


export default class AirforceWinner extends Component {
    render(){
        const userWinner = localStorage.getItem("userWinner");
        return(
            <div className="winner">
                <h1>
                Winner: Player {userWinner}!!!
                </h1>
            </div>
        )
    }

}