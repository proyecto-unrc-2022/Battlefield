import React, { useEffect, useState } from "react";
import { useNavigate } from "react-router-dom";
import authService from "../../services/auth.service";
import gameService from "../services/game.service";
import "../Styles.css"


{/*
    //Pagina que te permite seleccionar un personaje para una partida
*/}
export default function ChooseCharacter(){

    const [type, setType] = useState(null) 
    const [posX, setPosX] = useState(null)
    const [posY, setPosY] = useState(null)
    const [game, setGame] = useState([])

    const id_game = localStorage.getItem('id_game')

    const host = authService.getCurrentUser()

    const navigate = useNavigate();

    const redirec = () =>{
        navigate("/home_Infantry/wait_player");
    }

    const home = () =>{
        navigate("/home_Infantry");
    }

    const event = (e) =>{
        setType(e)
    }

    //Trae de la api los datos del juego
    const getGame = (id_game) =>{

        gameService.ready(id_game).then(resp =>{
            setGame(resp.data)
        }).catch(() =>{
            home()
        })

    }

    // validaciones a la hora de elegir una posicion para el personaje
    const validation = () => {

        if(posX == null || posY == null || posX == "" || posY == ""){
            alert("You must select the positions")
            setType(null)
            return false
        }

        if(0 > posY || posY > 10){
            alert("Its position in Y must be between 0 or 10")
            setType(null)
            return false

        }else{

            if(game.id_user1 === host.sub){

                if(0 > posX || posX > 9){
                    alert("Its position in X must be between 0 or 9")
                    setType(null)
                    return false
                }
            }
            if(game.id_user2 === host.sub){
                
                if(11 > posX || posX > 20){
                    alert("Its position in X must be between 11 or 20")
                    setType(null)
                    return false
                }
            }
        }

        return true
        
    }

    //Crea una figura y la guarda en la base de datos
    useEffect(() => {

        getGame(id_game)

        if(type){
            if(validation()){
                gameService.choose_figure(id_game, host.sub, type, parseInt(posX), parseInt(posY)).then(resp => {
                    console.log(resp.data)
                })
                redirec()

            }
        }
        
    }, [type])


    const handleInputChange_X = (e) =>{
        
        setPosX(e.target.value)
    }

    const handleInputChange_Y = (e) =>{
        setPosY(e.target.value)
    }

    //renderizacion de la pagina
    return(

        <div className="container-fluid d-flex justify-content-center">

            <div className="row jumbotron w-75 text-center mt-3">
                
                <div className="col">
                    <div className="">
                        <div id="carouselExampleControls" className="carousel slide" data-ride="carousel" data-interval="false">
                            <div className="carousel-inner">
                                <div className="carousel-item active">
                                    <img src="../Soldier.jpg" className="d-block w-100" alt="..."></img>
                                    <button type="button" className="btn btn-secondary mt-5 btn-lg" onClick={() => event(1)}>SOLDIER</button>
                                </div>
                                <div className="carousel-item">
                                    <img src="../Humvee.jpg" className="d-block w-100" alt="..."></img>
                                    <button type="button" className="btn btn-secondary mt-5 btn-lg" onClick={() => event(2)}>HUMVEE</button>
                                </div>
                                <div className="carousel-item">
                                    <img src="../Tank.jpg" className="d-block w-100" alt="..."></img>
                                    <button type="button" className="btn btn-secondary mt-5 btn-lg" onClick={() => event(3)}>TANK</button>
                                </div>
                                <div className="carousel-item">
                                    <img src="../Artillery.jpg" className="d-block w-100" alt="..."></img>
                                    <button type="button" className="btn btn-secondary mt-5 btn-lg" onClick={() => event(4)}>ARTILLERY</button>
                                </div>
                            </div>
                        <button className="carousel-control-prev" type="button" data-target="#carouselExampleControls" data-slide="prev">
                            <span className="carousel-control-prev-icon text-dark" aria-hidden="true"></span>
                            <span className="sr-only">Previous</span>
                        </button>
                        <button className="carousel-control-next" type="button" data-target="#carouselExampleControls" data-slide="next">
                            <span className="carousel-control-next-icon" aria-hidden="true"></span>
                            <span className="sr-only">Next</span>
                        </button>
                        </div>

                    </div> 
                </div>

                
                <div className="col-3 align-self-center text-center">
                    <div className="row mx-2">

                        <h2>X-position</h2>
                        <form>
                            <div className="form-row">
                                <div className="col-7 mx-1">
                                    <input type="number" 
                                    className="form-control" 
                                    
                                    onChange={handleInputChange_X}/>
                                </div>
                            </div>
                        </form>

                    </div>

                    <div className="row mt-3 mx-2">

                        <h2>Y-position</h2>
                        <form>
                            <div className="form-row">
                                <div className="col-7 mx-1">
                                    <input type="number" 
                                    className="form-control" 
                                    
                                    onChange={handleInputChange_Y}/>
                                </div>
                            </div>
                        </form>
                    </div>
                </div>

            </div>

            
        </div>

    )
}