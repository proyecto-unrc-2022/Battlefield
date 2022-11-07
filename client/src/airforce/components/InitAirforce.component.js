import { Button } from "bootstrap";
import React, { Component } from "react";
import { json } from "react-router-dom";
import Form from "react-validation/build/form";
import Input from "react-validation/build/input";
import AuthService from "../../services/auth.service";
import UserService from "../../services/user.service";
import airforceService from "../services/airforce.service";

import AirForceService from "../services/airforce.service"

export default class InitAirforce extends Component {
  constructor(props) {
    super(props)
    this.state = {
      user: 1,
      gameId: null,
    };
  }

  handleClik1 = () => {
    const game = AirForceService.createAirforceGame().then(
      () => {
        window.location.href = "/airforce/lobby";
      }
    )
  }
  // Para que ande este metodo, hay que lograr obtener la id del juego creado arriba, sino tira error
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
          <input  type="button" value="Create new game" onClick={this.handleClik1}/>
          <input type="button" value="Join in game" onClick={this.handleClick2}/>
       </form>
      </div>
    );
  }
}
