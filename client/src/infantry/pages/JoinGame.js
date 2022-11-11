import React, { useEffect, useState } from "react";
import { useNavigate } from "react-router-dom";
import gameService from "../services/game.service";
import "../Styles.css"


export default function JoinGame(){

    const navigate = useNavigate();

    const back= () =>{
        navigate("/home_Infantry");
    }

    const [games, setGames] = useState([])

    useEffect(() => {

        gameService.getGames().then((response) =>{
            setGames(response.data);
        })
    }, []);

    console.log(games)

    

    return(
        
        <div className="container bg-HomePage">
            
            <div className="row">
                <div className="col text-white">
                    <button onClick={back} type="button" className="btn btn-secondary m-3">Back</button>
                </div>
                
            </div>
            <div className="row">
                <div className="col-5"></div>
                <div className="col">
                <div className="col text-dark text-center d-flex justify-content-center flex-wrap">
                    
                    <h1 className="mb-3">Games Available</h1>
                    <ul className="Scroll list-group w-50">
                        {games.map(game => (  
                            <li className="list-group-item ">  
                                Games:{game.id} - User:{game.id_user1}  {/* */}
                            </li>  
                        ))}
                        
                    </ul>
                        
                </div>
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
        </div>
    )
    
}