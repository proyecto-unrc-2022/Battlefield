import React, { useState } from "react";
import { useParams } from "react-router-dom";
import AuthService from "../services/auth.service"
export default function UnderControls({setPosition}) {
    const params = useParams();
    const sessionId = params["id"];
    const user = AuthService.getCurrentUser().sub;

    function DirectionControl() {
        return (
            <div className="u-direction-container">
            </div>
        );
    }

    return (
        <div className="u-controls-container">
            <div className="u-left-controls">
                <DirectionControl />
            </div>
            <div className="u-right-controls">
                <span>Acá van los controles de acciones</span>
            </div>
        </div>
    );
}
