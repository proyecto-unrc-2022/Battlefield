import { Button } from "bootstrap";
import React, { Component } from "react";
import { Routes, Route, Link } from "react-router-dom";
import Form from "react-validation/build/form";
import Input from "react-validation/build/input";
import AirForceService from "../services/airforce.service"
import AuthService from "../../services/auth.service";


const TableHeader = () => {
  return(
    <thead style={{textAlign: "center"}}>
      <tr>
        <th>Games available</th>
      </tr>
    </thead>
  )
}

const TableBody = (props) => {
  const idGame = props.id
  return (
   <tbody>
      <tr>
        <td>
          {idGame}
        </td>
      </tr>
   </tbody> 
  )
}
export default class InitAirforce extends Component {

  state = {
    createdId: "",
    gameId: ""
  }

  newGameClik = () =>  {
    AirForceService.createAirforceGame().then(
      (response) => {
        const status_code = response.status;
        if (status_code === 200){
          this.props.callBack(response.data)
          console.log(response)
          this.setState({createdId: response.data.game_id})
          window.location.href = "/airforce/game/lobby"
        }
      },
        
    )
  }

  joinGameClick = () =>  {
    // alert('A name was submitted: ' + this.state.gameId);
    AirForceService.joinAirforceGame(this.state.gameId).then(
      (response) => {
        if (response.status === 200){
          window.location.href = "/airforce/game/lobby"
        }
      },
        
    )
  }

  // Para que ande este metodo, hay que lograr obtener el id del juego creado arriba, sino tira error
  handleChange(event) {    
    this.setState({gameId: event.target.value});  
  }

  handleClick2 = () => {
    window.location.reload(false);
    AirForceService.joinAirforceGame(3).then(
      (response) => {

        console.log(response);
        const status_code = response.status;
        if(status_code === 200){
          window.location.href = "/airforce/game/lobby"
        }
      }
    )
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
              onClick={this.newGameClik.bind(this)}>
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
            onClick={this.joinGameClick.bind(this)}>
            Join in game
          </button>
        </div>        
      </div>
    );
  }
}
