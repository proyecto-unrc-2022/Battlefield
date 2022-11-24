import React, { useEffect, useState } from "react";
import { useNavigate } from "react-router-dom";
import gameService from "../services/game.service";
import authService from "../../services/auth.service";
import "../Styles.css"
import Loading from "../components/Loading";

export default function CreateGame(){

    
    const [creatGame, setcreatGame] = useState([])
    const [gameWait, setGameWait] = useState([])
    
    const navigate = useNavigate();

    const event= () =>{
        navigate("/home_Infantry/choose_character");
    }

    const host = authService.getCurrentUser()

    const newGame = () =>{
        gameService.createGame(host.sub).then(response =>{
            setcreatGame(response.data)
        })
    }

    function wait(id){
        gameService.ready(id).then(response =>{
            setGameWait(response.data)
        })
    }

    useEffect(() => {
        newGame()
        
    },[])


    useEffect(() => {
        
        const timer = setTimeout(() => {
            wait(creatGame.id)
            console.log(gameWait)
            if(gameWait.id_user2 != null){
                event()
                localStorage.setItem("id_game", creatGame.id)
            }
        }, 8000);
        return () => clearTimeout(timer);
    }, [creatGame, gameWait]);

    return(
        <div className="container-fluid bg-HomePage ">
            
            <div className="row">
                
                <div className="col">
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
                
            </div>
            <div className="row">
                <div className="col-5"></div>
                
                <div className="col text-dark text-center">
                    
                    <Loading/>
                    
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