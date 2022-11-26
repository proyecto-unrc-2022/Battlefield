import React, { Component } from "react";
import GameBoard from "./gameBoard.component";
import FigureInfantryData from "./figureInfantryData.component";
import InfantryService from "../services/infantry.service"

import AuthService from "../../services/auth.service";
import GameOver from "./GameOver.component"


const EAST = 2
const SOUTH = 0
const SOUTH_EAST = 1
const SOUTH_WEST = 7
const WEST = 6
const NORTH_WEST = 5
const NORTH = 4
const NORTH_EAST = 3
function timeout(delay) {
  return new Promise( res => setTimeout(res, delay) );
}
/**
 * Renderiza la partida del juego actual
 */
export default class GameInfantry extends Component {
  constructor(props) {
    super(props);
    this.state = {
      game_id : props.game_id,
      game: null,
      figure: null,
      figureOpponent: null,
      projectiles: [],
      finished_round : false,
    }  
  }

    /**
     * Inicializa el juego y las figuras
     */
  componentDidMount(){
    let game = InfantryService.getGame(this.state.game_id)
    game.then(result => {
      this.setState({
        game: result
      })
      //figurePlayer1 siempre sera el AuthService.getCurrentUser().sub
      let figurePlayer1 = null
      let figurePlayer2 = null
      if(result["id_user1"] === AuthService.getCurrentUser().sub){
        figurePlayer1 = InfantryService.getFigure(result["id_user1"], this.state.game_id)
        figurePlayer2 = InfantryService.getFigure(result["id_user2"], this.state.game_id)
      }else{
        figurePlayer2 = InfantryService.getFigure(result["id_user1"], this.state.game_id)
        figurePlayer1 = InfantryService.getFigure(result["id_user2"], this.state.game_id)
      }
      figurePlayer1.then(result =>{
        this.setState({
          figure: result,
        })
      })
      figurePlayer2.then(result =>{
        this.setState({
          figureOpponent: result
        })
      })
    })
  }

  //Siempre esta verificando si el estado de finished_round es True para actualizar la ronda
  componentDidUpdate(prevState) {
    if(this.state.finished_round){
      this.updateRound()
    }
  }
  /**
   * Dada una accion(disparar o mover) le pega a la API con la correspondiente accion
   * @param {int} direction una direccion
   * @param {string} action una accion(move o shoot)
   * @param {int} velocity alcance de la accion(solo sirve para la accion mover, o para el proyectil de la artilleria)
   */
  action(direction, action, velocity){
    if(action === "move"){
        let response = InfantryService.move(this.state.game_id, AuthService.getCurrentUser().sub,
            direction, velocity)
        response.then( result => {
          if(result === "Accion invalida"){
            return alert("Movimiento invalido")
        }
          this.updateTurn();
          return;
        })
    }
    if(action === "shoot"){
        let response = InfantryService.shoot(this.state.game_id, AuthService.getCurrentUser().sub,
            direction)
        response.then(result => {
          if(result === "Accion invalida"){
            return alert("Movimiento invalido")
          }
          this.updateTurn();
          return;
        })
    }
  }

  /**
   * Actualiza el turno, y si acaba la ronda, cambia el estado de finished_round
   */
  updateTurn() {
    let data = InfantryService.next_turn(this.state.game_id);
    data.then(result => {
      if (result !== "Ronda terminada") {
        this.setState({
          turn: result["turn"]
        });
      }
      else {
        this.setState({
          finished_round: true
        });
      }
    });
  }
  /**
   * Se actualiza los projectiles y tambien las figuras(llamar solo si la ronda acabo)
   */
  async updateRound(){
    //Comienzo a actualizar los proyectiles y figuras en la API
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
      //Actualizo las figuras en this.state
      console.log(this.state.figure)
      let figurePlayer1 = await InfantryService.getFigure(this.state.figure["data"].id_user, this.state.game_id)
      let figurePlayer2 = await InfantryService.getFigure(this.state.figureOpponent["data"].id_user, this.state.game_id)
      let projectiles = await InfantryService.getProjectile(this.state.game_id)
      this.setState({
        figure: figurePlayer1,
        figureOpponent: figurePlayer2,
        finished_round:false,
        projectiles: projectiles
      })
      this.updateTurn()
  }
  /**
   * Dada la figura actual cuenta la cantidad de casillas que se puede mover
   * @returns devuelve en HTML la cantidad de casillas que se puede mover la figura del jugador
   */
  optionsRender(){
    const options = []
        for (let i = 0; i <= this.state.figure["data"].velocidad; i++) {
            options.push(<option value={i}>{i}</option>)
        }
    return options
}
/**
 * Muestra un mensaje dependiendo de la situacion de la ronda
 * @returns Retorna dos mensajes dependiendo de si acabo la ronda o no
 */
getMessageTurn() {
  let message;
  if (this.state.finished_round) {
    message = <h3 class="text-success">finished round!</h3>;
    //this.updateRound();
  }
  else {
    if(this.state.game.turn === AuthService.getCurrentUser().sub){
      message = <h3>Your turn</h3>
    }
    else{
      message = <h3>Opponent's turn</h3>
    }
  }
  return message
}

  render() {
    if(this.state.figure === null || this.state.figureOpponent === null
      || this.state.figure["data"] === undefined || this.state.figureOpponent["data"] === undefined
      ||this.state.figure["body"] === undefined || this.state.figureOpponent["body"] === undefined){
      return(
        <div class="container">
          <div class="row align-items-start">
            <div class="col"><br></br></div>
            <div class="col"><br></br><br></br><br></br><br></br><br></br><br></br><br></br><br></br><p class="d-flex justify-content-center">Cargando elementos...</p></div>
            <div class="col"><br></br></div>
          </div>
          <div class="row align-items-center">
            <div class="d-flex justify-content-center col">
              <div class="spinner-border" role="status">
                <span class="sr-only">Cargando elementos...</span>
              </div>
            </div>
          </div>       
        </div>
        
      )
    }
    else {
      return (
        <div>
          <div class="container-fluid bg-War">
            <div class="row align-items-start">
              <div class="col"><FigureInfantryData figure={this.state.figure["data"]} /></div>
              <div> <GameBoard figure={this.state.figure["body"]} figureOpponent={this.state.figureOpponent["body"]} projectiles={this.state.projectile}/></div>
              <div class="col"><FigureInfantryData figure={this.state.figureOpponent["data"]} /></div>
            </div>
            <p class="text-center">{this.getMessageTurn()}</p>
            <div class="row align-items-center">
              <div class="col"></div>
              <div class="container col">
                {/* Formulario para que el usuario elija que accion desea realizar */}
                <form onSubmit={ev => {ev.preventDefault();
                  this.action(ev.target.direction.value, ev.target.action.value, ev.target.velocity.value)}} >
                    {/* botones para seleccionar la direccion */}
                    <div class="form-group">
                        <div class="row align-items-start">
                            <div>
                                <input type="radio" class="btn-check col" name="direction" id="north west" autocomplete="off" checked value={NORTH_WEST} />
                                <label class="btn btn-secondary col" for="north west">North west</label>

                            </div>
                            <div>
                                <input type="radio" class="btn-check col" name="direction" id="north" autocomplete="off" checked value={NORTH} />
                                <label class="btn btn-secondary col" for="north">North</label>
                            </div>
                            <div>
                                <input type="radio" class="btn-check col" name="direction" id="north east" autocomplete="off" checked value={NORTH_EAST} />
                                <label class="btn btn-secondary col" for="north east">North east</label>
                            </div>
                        </div>

                        <div class="row align-items-center">
                            <div class="position-absolute top-50 start-50 translate-middle">
                                <input type="radio" class="btn-check" name="direction" id="west" autocomplete="off" checked value={WEST} />
                                <label class="btn btn-secondary" for="west">West</label>
                            </div>
                            <div class="col"></div>
                            <div class="col-7">
                                <div class="col aling-self-start">
                                    <input type="radio" class="btn-check col-md-4 aling-self-end" name="direction" id="east" autocomplete="off" checked value={EAST} />
                                </div>
                                <label class="btn btn-secondary col-3" for="east">East</label>
                            </div>
                        </div>

                        <div class="row align-items-end">
                            <div>
                                <label class="btn btn-secondary col" for="south west">South west</label>
                                <input type="radio" class="btn-check col" name="direction" id="south west" autocomplete="off" checked value={SOUTH_WEST} />
                            </div>
                            <div>
                                <label class="btn btn-secondary col " for="south">South</label>
                                <input type="radio" class="btn-check col" name="direction" id="south" autocomplete="off" checked value={SOUTH} />
                            </div>
                            <div>
                                <label class="btn btn-secondary col" for="south east">South east</label>
                                <input type="radio" class="btn-check col" name="direction" id="south east" autocomplete="off" checked value={SOUTH_EAST} />
                            </div>
                        </div>
                    </div>
                    {/* botones para seleccionar la accion */}
                    <div class="form-check">
                    <input class="form-check-input" type="radio" name="action" id="move" value={"move"} />
                        <label class="form-check-label text-white" for="move">
                            Move
                            <select class="form-select" id="sel1" name="velocity">
                                {this.optionsRender()}
                            </select>
                        </label>
                        <input class="form-check-input" type="radio" name="action" id="shoot" value={"shoot"} />
                        <label class="form-check-label text-white" for="shoot">
                            Shoot
                        </label>
                    </div>
                    <div class="text-center">
                      <ul class="list-group">
                        <li class="list-group-item">
                          <button type="submit" class="btn btn-outline-dark" disabled={this.state.finished_round || this.state.game.turn !== AuthService.getCurrentUser().sub}>Next turn</button>
                        </li>
                      </ul>
                    </div>
                  </form>
              </div>
              <div class="col"></div>
            </div>
            <p class="col"><GameOver game_id={this.state.game_id} player1_id={this.state.player1_id} player2_id={this.state.player2_id}></GameOver></p>
          </div>    
        </div>
      )
    }
  }
}
