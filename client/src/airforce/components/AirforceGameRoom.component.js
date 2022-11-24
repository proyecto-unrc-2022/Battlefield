import AirforceBoard from "./AirforceBoard.component";
import React, { Component } from "react";
import { useParams } from "react-router-dom";
import airforceService from "../services/airforce.service";

const GameRoom = () => {
    const {id} = useParams()
    
    const handleClickMoveNorth = () => {// course 1 north, 2 east, 3 south, 4 west
        airforceService.fligth(id,1);
    }
    const handleClickMoveEast = () => {// course 1 north, 2 east, 3 south, 4 west
        airforceService.fligth(id,2);
    }
    const handleClickMoveSouth = () => {// course 1 north, 2 east, 3 south, 4 west
        airforceService.fligth(id,3);
    }
    const handleClickMoveWest = () => {// course 1 north, 2 east, 3 south, 4 west
        airforceService.fligth(id,4);
    }

    const handleClickLaunchProjectile = () => {// course 1 north, 2 east, 3 south, 4 west
        airforceService.createProjectile(id);
    }
    
        return(
            <div className="battlefield">
                <div>
                    
                    <div>
                        {AirforceBoard(10,10)}
                    </div>
                    <div className="board-buttons">
                        <div className="action-buttons">
                            <form style={{display: "inline"}} onSubmit={e => e.preventDefault()}>
                                <button onClick = {handleClickMoveNorth} > Go North </button> 
                            </form>
                        </div>
                        <div className="action-buttons">
                            <form style={{display: "inline"}} onSubmit={e => e.preventDefault()}>
                                <button onClick = {handleClickMoveEast} > Go East </button> 
                            </form>
                        </div>
                        <div className="action-buttons">
                            <form style={{display: "inline"}} onSubmit={e => e.preventDefault()} >
                                <button onClick={handleClickMoveWest} > Go West </button> 
                            </form>
                        </div>
                        <div className="action-buttons">
                            <form style={{display: "inline"}} onSubmit={e => e.preventDefault()}>
                                <button onClick = {handleClickMoveSouth} > Go South </button> 
                            </form>
                        </div>
                        <div className="action-buttons">
                            <form style={{display: "inline"}} onSubmit={e => e.preventDefault()}>
                                <button onClick = {handleClickLaunchProjectile} > Launch Projectile </button>
                            </form>
                        </div>
                    </div>
                </div>
            </div>

        )
    }
export default GameRoom;