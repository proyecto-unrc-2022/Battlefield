import React, { useEffect, useState } from "react";
import { useNavigate } from "react-router-dom";
import Loading from "../components/Loading";
import gameService from "../services/game.service";
import "../Styles.css"

/*
    Pagina que espera que los dos jugadores hayan elegidos sus personajes
*/

export default function WaitPlayer(){

    const [game, setGame] = useState([])
    const [stateP1, setStateP1] = useState(false)
    const [stateP2, setStateP2] = useState(false)
    
    const id_game = localStorage.getItem('id_game')
    
    const navigate = useNavigate();

    const redirec = () =>{
        navigate("/infantry/game");
    }

    const home = () =>{
        navigate("/home_Infantry");
    }

    //Consulta los jugadores del game
    const getGame = () =>{

        gameService.ready(id_game).then(resp =>{
            setGame(resp.data)
        }).catch(() =>{
            home()
        })

    }

    //Consulta en la api si se creo correctamente la figura para el game para el jugador 1
    const state1 = () =>{
        gameService.character_wait(game.id, game.id_user1).then(resp =>{
            setStateP1(resp.data)
        })
    }

    //Consulta en la api si se creo correctamente la figura para el game para el jugador 2
    const state2 = () =>{
        gameService.character_wait(game.id, game.id_user2).then(resp =>{
            setStateP2(resp.data)
        })
    }


    useEffect(() =>{
        getGame()
    }, [])

    //Consulta cada 3 segundos el estado de los jugadores correspondiente al game
    useEffect(() =>{
        
        if(game?.id){

            const timer = setTimeout(() => {
                state1()
                state2()
                if(stateP1 !== false && stateP2 !== false){
                    redirec()
                }
            },3000)
            return () => clearTimeout(timer);   
        }
    }, [game, stateP1, stateP2])

    
    
    //Renderizacion de la pagina
    return(

        <div className="container-xl mt-5 ">
            
            <div className="row align-items-start">
                
                <div className="col text-dark text-center">

                    <br></br>
                    <br></br>
                    <br></br>
                    <br></br>
                    <br></br>
                    <br></br>
                        
                    <Loading/>
                        
                </div>
            </div>
        </div>

    )
}