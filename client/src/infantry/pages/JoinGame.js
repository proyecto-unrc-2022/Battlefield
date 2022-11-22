import React, { useEffect, useState } from "react";
import { useNavigate } from "react-router-dom";
import gameService from "../services/game.service";

import authService from "../../services/auth.service";
import "../Styles.css"


export default function JoinGame(){

    const navigate = useNavigate();

    const back= () =>{
        navigate("/home_Infantry");
    }

    const join= (idGame, idUser) =>{
        gameService.joinGame(idGame, idUser)
    }

    const [games, setGames] = useState([])

    const handleJoin = (uid) => {

        const game = games.filter((game) => game.id === uid)
        join(game[0].id, host.sub)

    }



    const get_Games = () => {

         return(<div className="row">
                <div className="col-5"></div>
                <div className="col">
                <h1 className="mb-4 text-center Battlefield-Infantry">Games Available</h1>
                <div className="col rounded-5 text-center d-flex justify-content-center">
                    
                    
                    <ul className="Scroll list-group w-50">
                        {games.map(game => (  
                            <li onClick={() => handleJoin(game.id)} key={game.id} className=" list-group-item ">  
                                Games:{game.id} - User:{game.id_user1} -  {/* */}
                                
                                <button type="button" className="btn btn-secondary" onClick={() => handleJoin(game.id)}>Join</button>
                            </li>
                        ))}

                        
                    </ul>
                </div>
                </div>
        </div>)


    }

    const get = () => {

        gameService.getGames().then((response) =>{
            setGames(response.data);
        })


    }

    useEffect(() => {
        get()
    }, []);    

    const host = authService.getCurrentUser()    

    return(
        
        <div className="container-fluid bg-HomePage">
            
            <div className="row">
                <div className="col text-white">
                    <button onClick={back} type="button" className="btn btn-secondary m-3">Back</button>
                </div>
                
            </div>

            {get_Games()}

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