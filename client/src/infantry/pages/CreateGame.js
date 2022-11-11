import React from "react";
import { useNavigate } from "react-router-dom";
import "../Styles.css"

export default function CreateGame(){

    const navigate = useNavigate();

    const back= () =>{
        navigate("/home_Infantry");
    }

    return(
        <div className="container bg-HomePage">
            
            <div className="row">
                <div className="col text-white">
                    <button onClick={back} type="button" className="btn btn-secondary m-3">Back</button>
                    
                </div>
                
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