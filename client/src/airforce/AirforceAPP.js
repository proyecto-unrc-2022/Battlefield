import React, { Component } from "react";
import { Routes, Route, Link } from "react-router-dom";
import "bootstrap/dist/css/bootstrap.min.css";
import InitAirforce from "./components/InitAirforce.component";
import AirforceLobby from "./components/AirforceLobby.component";



class AirforceAPP extends Component {

    state = {
        gameInfo: "",
    }

    handleCallback = (childData) => {
        this.setState({gameInfo: childData.game_id})
    }

    render() {
        return (
        <div className="container mt-3">
            <Routes>
                <Route path="/airforce" element={<InitAirforce callBack={this.handleCallback}/>}/>
                <Route path="/airforce/lobby" element={<AirforceLobby gameId={this.state.gameInfo}/>}/>
            </Routes>
        </div>
    )}
}


export default AirforceAPP;