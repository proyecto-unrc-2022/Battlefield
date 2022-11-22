import React, { Component } from "react";
import TableGame from "./tableGame.component";
import FigureInfantryData from "./figureInfantryData.component";
import InfantryService from "../services/infantry.service"
import GameInfantryData from "./gameInfantryData.component";
import FigureActions from "./figureActions.component";

export default class GameInfantry extends Component {
  constructor(props) {
    super(props);
    this.state = {
      game_id : props.game_id,
      player1_id: null,
      player2_id: null,
      turn: null
    }  
  }

  async componentDidMount(){
    let game = await InfantryService.getGame(this.state.game_id)
    this.setState({
      player1_id: game["id_user1"],
      player2_id: game["id_user2"],
      turn : game["turn"]
    })
  }

  render() {
    if(this.state.player1_id === null){return;}
    return (
      <div>
        <div class="container">
          <div class="row align-items-start">
            <div class="col"><FigureInfantryData game_id={this.state.game_id} user_id={this.state.player1_id} /></div>
            <div> <TableGame game_id={this.state.game_id} player1_id={this.state.player1_id} player2_id={this.state.player2_id}/></div>
            <div class="col"><FigureInfantryData game_id={this.state.game_id} user_id={this.state.player2_id} /></div>
          </div>
          <div class="row align-items-center">
             <p class="col"><FigureActions game_id={this.state.game_id} user_id={this.state.player1_id}></FigureActions> </p>
            <GameInfantryData class="col align-self-center" turn={this.state.turn} game_id={this.state.game_id}/> 
            <p class="col"><FigureActions game_id={this.state.game_id} user_id={this.state.player2_id}></FigureActions></p>
          </div>
        </div>    
      </div>
    )
  }
}
