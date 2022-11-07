import React, { Component } from "react";
import { Routes, Route, Link } from "react-router-dom";
import "bootstrap/dist/css/bootstrap.min.css";
import InitAirforce from "./components/InitAirforce.component";
import AirforceLobby from "./components/AirforceLobby.component";


class AirforceAPP extends Component {
    render() {
        return (
        <div className="container mt-3">
            <Routes>
                <Route path="/airforce" element={<InitAirforce />}/>
                <Route path="/airforce/lobby" element={<AirforceLobby />}/>
            </Routes>
        </div>
    )}
}


export default AirforceAPP;