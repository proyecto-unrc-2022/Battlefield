import { Button } from "bootstrap";
import React, { Component } from "react";
import { Routes, Route, Link } from "react-router-dom";
import AirForceService from "../services/airforce.service"
import "./AirforceMainMenu.css"

export default class AirforceMainMenu extends Component {

  state = {
    createdId: "",
    gameId: ""
  }

  handleNewGameClik = () =>  {
    AirForceService.createAirforceGame().then(
      (response) => {
        const status_code = response.status;
        if (status_code === 200){
          this.props.callBack(response.data)
          console.log(response)
          this.setState({createdId: response.data.game_id})
          window.location.href = "/airforce/game/lobby/"+response.data.game_id
        }
      },
        
    )
  }

  handleJoinGameClick = () =>  {
    // alert('A name was submitted: ' + this.state.gameId);
    AirForceService.joinAirforceGame(this.state.gameId).then(
      (response) => {
        if (response.status === 200){
          window.location.href = "/airforce/game/lobby/"+this.state.gameId;
        }
      },
        
    )
  }

  handleChange(event) {    
    this.setState({gameId: event.target.value});  
  }

  render() {
    return (
      <div className= "af-container" style={{textAlign: "center"}}>
      <link href='https://fonts.googleapis.com/css?family=Silkscreen' rel='stylesheet'></link>
        <h1 className="af-title">
          Air Force Game
        </h1>
        
        <div>
          <button
              className="create-game" 
              type="button" 
              onClick={this.handleNewGameClik.bind(this)}>
              Create new game
          </button>
        </div>
        <div>
          <div>
          <input className="id-game"
                  type="text"
                  placeholder="Game id"
                  style={{textAlign: "center"}}
                  name="Game id" required 
                  id="Game id"
                  onChange={this.handleChange.bind(this)}
          />
          </div>
          <button
            className="join-game" 
            type="button" 
            onClick={this.handleJoinGameClick.bind(this)}>
            Join in game
          </button>
        </div>        
      </div>
    );
  }
}
