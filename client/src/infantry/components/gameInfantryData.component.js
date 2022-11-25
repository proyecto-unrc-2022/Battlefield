import React, { Component } from "react";
import InfantryService from "../services/infantry.service"


function timeout(delay) {
  return new Promise( res => setTimeout(res, delay) );
}

export default class GameInfantryData extends Component {
    constructor(props) {
      super(props);
      this.state = {
        game_id : this.props.game_id,
        turn: this.props.turn,
        finished_round : false
      }
    }

    // async componentDidMount(){
    //   let game = await InfantryService.getGame(this.state.game_id)
    //   this.setState({
    //     turn : game["turn"]
    //   })
    // }

    // async componentDidUpdate(prevProps, prevState){
    //   let game = await InfantryService.getGame(this.state.game_id)

    //     this.setState({
    //       turn : game["turn"]
    //     })
    //     //console.log("componentDidUpdate")

    // }
    // async shouldComponentUpdate(nextProps) {
    //   // Rendering the component only if 
    //   // passed props value is changed
    //   let game = await InfantryService.getGame(this.state.game_id)
    //   //console.log(game["turn"])
    //   if (nextProps.turn !== game["turn"]) {
    //     return true;
    //   }
    //   return false;
    // }

    async updateTurn() {
      let data = await InfantryService.next_turn(this.state.game_id)
      if( data !== "Ronda terminada"){
        this.setState({
          turn: data["turn"]
        })
      }
      else{
        this.setState({
          finished_round:true
        })
      }
    }
    async updateRound(){
      let is_there_projectiile = ""
      while (is_there_projectiile !== "empty update projectiles queue"){
        is_there_projectiile = await InfantryService.update_projectiles(this.state.game_id)
        await timeout(1000)
      }
      let is_there_actions = ""
      while (is_there_actions !== "no actions in queue"){
        is_there_actions = await InfantryService.update_actions(this.state.game_id)
        await timeout(1000)
      }
        this.setState({
          finished_round:false
        })
        this.updateTurn()
    }
  render(){
    let message
    
    if(this.state.finished_round){
      message =  <h3 class="text-success">finished round!</h3>
      this.updateRound()
    }
    else{
      message = <h3>Player {this.state.turn}'s turn</h3>
    }
    
    return(
    <div class="text-center">
      <ul class="list-group">
        <li class="list-group-item">
            {message}
            <button onClick={() =>{this.updateTurn()}} disabled={this.state.finished_round} class="btn btn-outline-dark">Next turn</button>
        </li>
      </ul>
    </div>)
    
   
  }
}