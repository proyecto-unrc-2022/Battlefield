import React, { useState } from "react";
import { useParams } from "react-router-dom";
import AuthService from "../services/auth.service"
export default function UnderControls({position, setPosition}) {
    const params = useParams();
    const sessionId = params["id"];
    const user = AuthService.getCurrentUser().sub;

    function DirectionControl({position, setPosition}) {
        const rotation = 45 * position.direction;

        const style = {
            transform: "rotate(" + rotation + "deg)",
        }

        function setDirection (dir){
            setPosition({x: position.x, y: position.y, direction: dir});
        }
        
        const array1 = [7,0,1,6];
        const array2 = [2,5,4,3];

        return (
            <div style={{position: 'relative', height: 157, width: 157}}>
                <img style={style} className="u-overlap-1" src={require('./css/direc.png')} width="100%" />
                <div className="u-overlap-2 u-direction-grid">
                    {array1.map(i => {return (<div style = {{height: "100%", width: "100%"}} onClick={_ => setDirection(i)}></div>)})}
                    <div style={{height: '100%', width: '100%'}}></div>
                    {array2.map(i => {return (<div style = {{height: "100%", width: "100%"}} onClick={_ => setDirection(i)}></div>)})}
                </div>
            </div>
        );
    }

    return (
        <div className="u-controls-container">
            <div className="u-left-controls">
                <DirectionControl position={position} setPosition={setPosition}/>
            </div>
            <div className="u-right-controls">
                <span>Acá van los controles de acciones</span>
            </div>
        </div>
    );
}
