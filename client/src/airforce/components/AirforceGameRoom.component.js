import AirforceBoard from "./AirforceBoard.component";
import React, { Component } from "react";
import { useParams } from "react-router-dom";
import airforceService from "../services/airforce.service";
import "./AirforceGameRoom.css"

const GameRoom = () => {
    const {id} = useParams();
    var boardInfo = [];
    var round = 0;
    var userInfo = {};

    const handleClickMoveNorth = () => {// course 1 north, 2 east, 3 south, 4 west
        airforceService.fligth(id,1)
    }
    const handleClickMoveEast = () => {// course 1 north, 2 east, 3 south, 4 west
        airforceService.fligth(id,2)
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


    const boardStatus = () => {

        airforceService.getBoardStatus(id)
        .then((response) => {
            localStorage.setItem("boardStatus", JSON.stringify(response.data));
        });
        round = round + 1;
        boardInfo = localStorage.getItem("boardStatus");
   
        airforceService.getPlayerPlane(id).then((response) => {
            localStorage.setItem("playerPlane", JSON.stringify(response.data));
        })
        userInfo = JSON.parse(localStorage.getItem("playerPlane"));
        console.log(userInfo);
    }

    setInterval(() => {
        airforceService.getBoardStatus(id).then(
            (response) => {
                console.log(response.data.status)
                if (response.data.status === "end") {
                    window.location.href = "/airforce/game/"+id+"/winner";
                    localStorage.setItem("userWinner", response.data.Winner)
                    
                } 
            }
        )
    }, 5000);
   
        return(
            <div className="battlefield">
                <div>
                    <div>
                        {boardStatus()}
                    </div>
                    <div>{  
                            AirforceBoard(boardInfo, round)
                        }
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
                <div className="PlaneTitle" >
                    <div>
                        Plane = <h className="PlaneInfo">{userInfo.name}</h> 
                    </div>   
                    <div>
                        Health = <h className="PlaneInfo">{userInfo.health}</h> 
                    </div>
                    <div>    
                        Projectiles = <h className="PlaneInfo">{userInfo.cant_projectile}</h> 
                    </div>
                </div>
            </div>

        )
    }
export default GameRoom;