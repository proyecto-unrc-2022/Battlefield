import React, { useEffect, useState } from "react";
import { useNavigate } from "react-router-dom";
import Loading from "../components/Loading";
import gameService from "../services/game.service";
import "../Styles.css"

export default function WaitPlayer(){

    const [game, setGame] = useState([])
    const [stateP1, setStateP1] = useState(false)
    const [stateP2, setStateP2] = useState(false)
    
    const id_game = localStorage.getItem('id_game')
    
    const navigate = useNavigate();

    const redirec = () =>{
        navigate("/home_Infantry");
    }

    const getGame = () =>{

        gameService.ready(id_game).then(resp =>{
            setGame(resp.data)
        })

    }

    const state1 = () =>{
        gameService.character_wait(game.id, game.id_user1).then(resp =>{
            setStateP1(resp.data)
        })
    }

    const state2 = () =>{
        gameService.character_wait(game.id, game.id_user2).then(resp =>{
            setStateP2(resp.data)
        })
    }

    useEffect(() =>{
        getGame()
    }, [])

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