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

    const back= () =>{
        navigate("/home_Infantry");
        gameService.removeGame(creatGame.id).then(resp =>{
            console.log(resp)
        })

    }

    const host = authService.getCurrentUser()

    //Crea un nuevo juego en la base de datos
    const newGame = () =>{
        gameService.createGame(host.sub).then(response =>{
            setcreatGame(response.data)
        })
    }

    //Consulta a la api el estado del juego
    function wait(id){
        gameService.ready(id).then(response =>{
            setGameWait(response.data)
        })
    }


    useEffect(() => {
        newGame()
        
    },[])

    //Cada 3 seg consulta a la base de datos si un jugador se unió
    useEffect(() => {
        
        const timer = setTimeout(() => {
            wait(creatGame.id)
            console.log(gameWait)
            if(gameWait.id_user2 != null){
                event()
                localStorage.setItem("id_game", creatGame.id)
            }
        }, 3000);
        return () => clearTimeout(timer);
    }, [creatGame, gameWait]);

    //renderizacion de la pagina
    return(
        <div className="container-fluid bg-HomePage ">

            <div className="col text-white">
                    <button onClick={back} type="button" className="btn btn-secondary m-3">Back</button>
            </div>
            
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