import { Button } from "bootstrap";
import React, { Component } from "react";
import { Routes, Route, Link } from "react-router-dom";
import AirForceService from "../services/airforce.service"




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
        const status_code = response.status;
        if (status_code === 200){
          this.props.callBack(response.data)
          console.log(response)
          this.setState({createdId: response.data.game_id})
          window.location.href = "/airforce/lobby"
        }
      },
        
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
      (response) => {
        const status_code = response.status;
        if(status_code === 200){
          window.location.href = "/airforce/game/lobby"
        }
      }
    )
  }


  render() {
    const {gameId} = this.state;
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
              onClick={this.handleClik1.bind(this)}>
              Create new game
          </button>
        </div>
        <div>
          <form>
             <div>
                  <input className="id-game"
                  type="text"
                  placeholder="Game id"
                  style={{textAlign: "center"}}
                  name="Game id" required 
                  id="Game id"
                  value={gameId}
                  onChange={this.handleChange.bind(this)}/>
              </div>
              <div>
                <input className="join-game" 
                  type="submit" 
                  value="Join game" 
                  onClick={this.handleClick2.bind(this)}/>
              </div>
          </form>
        </div>
      </div>
    );
  }
}
