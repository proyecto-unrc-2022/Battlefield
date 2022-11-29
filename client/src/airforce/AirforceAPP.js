import React, { Component } from "react";
import { Routes, Route, Link } from "react-router-dom";
import "bootstrap/dist/css/bootstrap.min.css";
import AirforceMainMenu from "./components/AirforceMainMenu.component";




class AirforceAPP extends Component {

    state = {
        gameInfo: "",
    }

    handleCallback = (childData) => {
        this.setState({gameInfo: childData.game_id})
    }

    render() {
        return (
        <div>
            <AirforceMainMenu callBack={this.handleCallback}/> 
        </div>
    )}
}


export default AirforceAPP;