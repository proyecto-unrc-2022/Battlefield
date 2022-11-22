import React, { useEffect } from "react";
import { useNavigate } from "react-router-dom";
import gameService from "../services/game.service";
import authService from "../../services/auth.service";
import "../Styles.css"

export default function CreateGame(){

    const navigate = useNavigate();

    const back= () =>{
        navigate("/home_Infantry");
    }

    const host = authService.getCurrentUser()

    useEffect(() => {

        gameService.createGame(host.sub)

    },[])

    return(
        <div className="container-fluid bg-HomePage ">
            
            <div className="row">
                
                
            </div>
            <div className="row">
                <div className="col-5"></div>
                
                <div className="col text-dark text-center">
                    
                    sad
                    
                </div>
                
            </div>
            <br></br>
            <br></br>
            <br></br>
            <br></br>
            <br></br>
            <br></br>
            <br></br>
            <br></br>
            <br></br>
            <br></br>
            <br></br>
            <br></br>
            <br></br>
            <br></br>
            <br></br>
            <br></br>
            <br></br>
            <br></br>
            <br></br>
            <br></br>
            <br></br>
            <br></br>
        </div>
    )
    
}