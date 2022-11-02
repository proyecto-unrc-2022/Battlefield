import React, { Component } from "react";
import { Routes, Route, Link } from "react-router-dom";
import "bootstrap/dist/css/bootstrap.min.css";
import InitAirforce from "./components/InitAirforce.component";

class AirforceAPP extends Component {
    render() {
        return (<div className="container mt-3">
            <Routes>
            <Route path="/airforce" element={<InitAirforce />} />
            </Routes>
        </div>
    )}
}


export default AirforceAPP;