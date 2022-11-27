import React, { useEffect, useState } from "react";
import { useNavigate } from "react-router-dom";
import authService from "../../services/auth.service";
import gameService from "../services/game.service";
import "../Styles.css"

export default function ChooseCharacter(){

    const [type, setType] = useState(null)
    const [posX, setPosX] = useState(null)
    const [posY, setPosY] = useState(null)
    const [game, setGame] = useState([])

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

    const getGame = (id_game) =>{

        gameService.ready(id_game).then(resp =>{
            setGame(resp.data)
        }).catch(() =>{
            home()
        })

    }

    const validation = () => {
        if(0 > posY || posY > 10){
            alert("Su posicion en Y debe ser entre 0 o 10")
            setType(null)
            return false

        }else{

            if(game.id_user1 === host.sub){

                if(0 > posX || posX > 9){
                    alert("Su posicion en X debe ser entre 0 o 9")
                    setType(null)
                    return false
                }
            }
            if(game.id_user2 === host.sub){
                
                if(11 > posX || posX > 20){
                    alert("Su posicion en X debe ser entre 11 o 20")
                    setType(null)
                    return false
                }
            }
        }

        return true
        
    }

    const id_game = localStorage.getItem('id_game')

    const host = authService.getCurrentUser()

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

    return(

        <div className="container">

            <div className="row jumbotron text-center mt-3">
                
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
                                    <img src="../ARTILLERY.jpg" className="d-block w-100" alt="..."></img>
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
                                <div className="col-7">
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
                                <div className="col-7">
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