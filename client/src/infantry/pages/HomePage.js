import React from "react";
import { useNavigate } from "react-router-dom";
import "../Styles.css"

export default function HomePage(){

    const navigate = useNavigate();

    const navigateCreate_game= () =>{
        navigate("create_game");
    }

    const navigateJoin_game= () =>{
        navigate("join_game");
    }

    //Renderizaciones de la pagina
    return(

        
        <div className="container-fluid bg-HomePage">
            <div className="text-center ">
                <br></br>
                <br></br>
                <div className="row">

                    <div className="col-5"></div>

                    <div className="col align-self-center">
                        <br></br>
                        <br></br>
                        <br></br>
                        <br></br>
                        
                        
                        <h1 className="Battlefield-Infantry text-center mt-5 ">Battlefield Infantry</h1>
                        <br></br>
                        {localStorage.removeItem("id_game")}
                        <button onClick={navigateCreate_game} type="button" className="btn btn-secondary mr-3 mb-4">Create Game</button>
                        <button onClick={navigateJoin_game} type="button" className="btn btn-secondary mr-3 mb-4">Join Game</button>
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
                    

            </div>
            
        </div>
    )

    
}




