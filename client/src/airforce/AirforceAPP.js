import React, { Component } from "react";
import { Routes, Route, Link } from "react-router-dom";
import "bootstrap/dist/css/bootstrap.min.css";
import InitAirforce from "./components/InitAirforce.component";
import AirforceLobby from "./components/AirforceLobby.component";
import "./index.css"



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
        
            <InitAirforce callBack={this.handleCallback}/> 
        </div>
    )}
}


export default AirforceAPP;