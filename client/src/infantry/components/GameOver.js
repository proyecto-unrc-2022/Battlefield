import React, { Component } from "react";
import InfantryService from "../services/infantry.service";
import gameOver from "./gameOver.png";


function GameOver(figure1, figure2) {

    if(figure1.hp <= 0 || figure2.hp <= 0)

        return <div>
                    <img src={gameOver}/>
               </div>
}

export default class FigureActions extends Component (){
    constructor(props) {
        super(props);
        this.state = {
          game_id: props.game_id,
          player1_id: props.player1_id,
          player2_id: props.player2_id,
          figure1: null,
          figure2: null,
          projectiles: null
        }
    }

render(){

    return <div> {this.state.GameOver(this.state.figure1, this.state.figure2)}  </div>

}
}
