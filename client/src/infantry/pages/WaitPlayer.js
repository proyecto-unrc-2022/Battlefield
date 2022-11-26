import React, { useEffect, useState } from "react";
import { useNavigate } from "react-router-dom";
import Loading from "../components/Loading";
import gameService from "../services/game.service";
import "../Styles.css"

export default function WaitPlayer(){

    const [game, setGame] = useState([])
    const [state, setState] = useState(null)
    
    const navigate = useNavigate();

    const redirec = () =>{
        navigate("/home_Infantry");
    }

    const id_game = localStorage.getItem('id_game')

    const getGame = () =>{

        gameService.ready(id_game).then(resp =>{
            setGame(resp.data)
        })

    }


    useEffect(() =>{

        getGame()
        

    }, [])

    useEffect(() =>{
        if(game){
            console.log(game.id)
            console.log(game.id_user1)
            console.log(game.id_user2)
            gameService.character_wait(game.id, game.id_user2).then(resp =>{
                setState(resp.data)
            })
            
        }
    },[game])
 
    const figure = (id_user) =>{

        gameService.character_wait(game.id, id_user).then(resp =>{
            setState(resp)
        })

        if(state === null){
            return false
        }else{
            return true
        }
    } 
    
    
    
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