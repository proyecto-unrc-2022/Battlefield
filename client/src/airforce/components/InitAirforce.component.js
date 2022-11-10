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

  handleClik1 = () =>  {
    AirForceService.createAirforceGame().then(
      (response) => {
        this.props.callBack(response.data)
        this.setState({createdId: response.data.game_id})
      },
      window.location.href = "/airforce/game/lobby"

    )
  }
  // Para que ande este metodo, hay que lograr obtener el id del juego creado arriba, sino tira error
  handleChange = (event) => {
    const { name, value } = event.target
    this.setState({
      gameId: value,
    })
    console.log(this.state)

  }

  handleClick2 = () => {
    AirForceService.joinAirforceGame(this.state.gameId).then(
      () => {
        window.location.href = "/airforce/game/lobby";
      }
    )
  }


  render() {
    const {gameId} = this.state;
    return (
      <div className="airforce-bg">
       <h1 className="af-title"
        style={{textAlign: "center"}}>Air Force Game</h1>

       <input className="create-game" 
          type="button" 
          value="Create new game" 
          onClick={this.handleClik1.bind(this)}/>
       <form>
          <input className="join-game" 
            type="submit" 
            value="Join game" 
            onClick={this.handleClick2}/>
            <input className="id-game"
            type="text"
            placeholder="Game id"
            name="Game id" required 
            id="Game id"
            value={gameId}
            onChange={this.handleChange}/>
       </form>
        <table style={{marginLeft: 800, marginTop: -50}}>
         <TableHeader />
         <TableBody id={this.state.createdId}/>
       </table> 
       
      </div>
    );
  }
}
