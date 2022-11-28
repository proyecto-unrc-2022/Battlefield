import React, { useEffect, useState } from "react";
import { useNavigate } from "react-router-dom";
import gameService from "../services/game.service";

import authService from "../../services/auth.service";
import "../Styles.css"

/*
    Pagina que permite unirse a un game
 */


export default function JoinGame(){

    const [users, setUsers] = useState([])
    const [games, setGames] = useState([])

    const host = authService.getCurrentUser()    

    const navigate = useNavigate();

    const back= () =>{
        navigate("/home_Infantry");
    }

    const redirc = () =>{
        navigate("/home_Infantry/choose_character");
    }

    //Realiza una post para que un jugador se una al game
    const join= (idGame, idUser) =>{
        gameService.joinGame(idGame, idUser)
    }    

    const handleJoin = (id) => {

        const game = games.filter((game) => game.id === id)
        if(game[0].id_user1 !== host.sub){
            join(game[0].id, host.sub)
            localStorage.setItem("id_game", game[0].id)
            redirc()
        }else{
            alert("No puedes ingresar a tu propia partida")
        }
        

    }

    //Muestra los games disponibles, con su usuario creador
    const get_Games = () => {
        
         return(<div className="row">
                <div className="col-5"></div>
                <div className="col">
                <h1 className="mb-4 text-center Battlefield-Infantry">Games Available</h1>
                <div className="col rounded-5 text-center d-flex justify-content-center">
                    
                {localStorage.removeItem("id_game")}
                    <ul className="Scroll list-group w-50">
                        {games.map(game => (  
                            <li key={game.id} className=" list-group-item ">

                                Games:{game.id} - User: {users.find(elem => elem.id === game.id_user1).username} -  {/* */}
                                
                                <button type="button" className="btn btn-secondary" onClick={() => handleJoin(game.id)}>Join</button>
                            </li>
                        ))}

                        
                    </ul>
                </div>
                </div>
        </div>)


    }

    //Trae de la api todos los games
    const get = () => {

        gameService.getGames().then((response) =>{
            setGames(response.data);
        })
    }

    //Trae de la api todos los users
    useEffect(() =>{

        gameService.getUsers().then((response) =>{
            setUsers(response.data);
        })
    },[])

    useEffect(() => {
        if(users[0]){
            get()
        }
    }, [users]);

    //Renderizacion de la pagina 
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