import React, { Component } from "react";
import InfantryService from "../services/infantry.service"

export default class GameInfantryData extends Component {
    constructor(props) {
      super(props);
      this.state = {
        turn: this.props.turn,
      }
    }
    async componentDidMount(){

    }
  render(){
    return(
    <div>
      <h3>Player {this.props.turn}'s turn</h3>
      <button>Next turn</button>
    </div>)
    
   
  }
}