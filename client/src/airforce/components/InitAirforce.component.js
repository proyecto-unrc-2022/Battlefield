import { Button } from "bootstrap";
import React, { Component } from "react";
import { json } from "react-router-dom";
import Form from "react-validation/build/form";
import Input from "react-validation/build/input";
import AuthService from "../../services/auth.service";
import UserService from "../../services/user.service";
import AirForceService from "../services/airforce.service"

export default class InitAirforce extends Component {
  constructor(props) {
    super(props);
    this.state = {
      gameId: "",
    };
  }


  handleClik1() {
    AirForceService.createAirforceGame().then(
      (response) => {
        this.setState({
          gameId: response.data,
        }); 
      },
      window.location.href = "/airforce/lobby"
    )
  }
  // Para que ande este metodo, hay que lograr obtener el id del juego creado arriba, sino tira error
  handleClick2 = () => {
    AirForceService.joinAirforceGame().then(
      () => {
        window.location.href = "/airforce/lobby";
      }
    )
  }

  render() {
    return (
      <div>
       <h1 style={{textAlign: "center"}}>Air Force Game</h1>
       <form>
          <input 
            className="createGame" 
            type="button" 
            value="Create new game" 
            onClick={this.handleClik1.bind(this)}

          />
          <label>Game id:</label>
          <input type="text" name="Game id" id="Game id" required/>

          <input className="joinGame" type="button" value="Join game" onClick={this.handleClick2.bind(this)}/>
       </form>
      </div>
    );
  }
}
