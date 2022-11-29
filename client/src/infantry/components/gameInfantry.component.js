import React, { Component } from "react";
import GameBoard from "./gameBoard.component";
import FigureInfantryData from "./figureInfantryData.component";
import InfantryService from "../services/infantry.service"

import AuthService from "../../services/auth.service";
import gameOver from "../images/gameOver.png"
import gameService from "../services/game.service";



const EAST = 2
const SOUTH = 0
const SOUTH_EAST = 1
const SOUTH_WEST = 7
const WEST = 6
const NORTH_WEST = 5
const NORTH = 4
const NORTH_EAST = 3


/**
 * Renderiza la partida del juego actual
 */
export default class GameInfantry extends Component {
  constructor(props) {
    super(props);
    this.state = {
      game_id: localStorage.getItem("id_game"),
      game: null,
      figure: null,
      figureOpponent: null,
      projectiles: [],
      next_turn: false, //principalmente utilizado para shouldComponentUpdate()
      finished_round: false
    }
    this.timer = null;
  }

   


  /**
   * Inicializa el juego y las figuras
   */
  componentDidMount() {
    let game = InfantryService.getGame(this.state.game_id)
    game.then(result => {
      this.setState({
        game: result
      })
      //figurePlayer1(figure) siempre sera el AuthService.getCurrentUser().sub
      //figurePlayer2(figureOpponent) siempre sera la figura oponente
      let figurePlayer1 = null
      let figurePlayer2 = null
      let projectiles = InfantryService.getProjectile(this.state.game_id)
      console.log(this.state.game_id)
      projectiles.then(result => {
        this.setState({
          projectiles: result
        })
      })
      if (result["id_user1"] === AuthService.getCurrentUser().sub) {
        figurePlayer1 = InfantryService.getFigure(result["id_user1"], this.state.game_id)
        figurePlayer2 = InfantryService.getFigure(result["id_user2"], this.state.game_id)
      } else {
        figurePlayer2 = InfantryService.getFigure(result["id_user1"], this.state.game_id)
        figurePlayer1 = InfantryService.getFigure(result["id_user2"], this.state.game_id)
      }
      figurePlayer1.then(result => {
        this.setState({
          figure: result,
        })
      })
      figurePlayer2.then(result => {
        this.setState({
          figureOpponent: result
        })
      })
    })
  }

  componentDidUpdate() {
    if (this.state.game !== null && this.state.figureOpponent !== null
      && this.state.figure !== null) {
      //Cada 3 segundo pregunta sobre el estado del otro jugador y del juego
      //Esto es util para cuando no es tu turno
      //Se utiliza un timer para no hacer un llamado masivo a la API
      this.timer = setTimeout(async () => {
        let nextGame = await InfantryService.getGame(this.state.game_id)
        if (AuthService.getCurrentUser().sub === nextGame.turn) {
          //Entra solo cuando el oponente termina con su turno
          this.setState({
            next_turn: false
          });
        }
        this.setState({
          game: nextGame,
        });
        //Cada tanto revisa las posiciones de las figuras y proyectiles
        //para saber si el oponente finalizo la ronda
        let nextFigurerOpponent = await InfantryService.getFigure(this.state.figureOpponent["data"].id_user, this.state.game_id)
        let nextProjectiles = await InfantryService.getProjectile(this.state.game_id)
        //Se compara si el estado actual de tus proyectiles y figuras es diferente
        //al estado actual del juego en la API
        let equalsProjectiles = true // true si this.state.proyecttiles === nextProyectiles, false en caso contrario
        if (this.state.projectiles.length === 0 && nextProjectiles.length > 0) {
          equalsProjectiles = false
        }
        else if (this.state.projectiles.length > 0 && nextProjectiles.length === 0) {
          equalsProjectiles = false
        }
        else if(this.state.projectiles.length > nextProjectiles.length){
          equalsProjectiles = false
        }
        else if(this.state.projectiles.length < nextProjectiles.length){
          equalsProjectiles = false
        }
        else if (this.state.projectiles.length === nextProjectiles.length) {
          equalsProjectiles = this.state.projectiles.every((value, index) => {
            return (value.pos_x === nextProjectiles[index].pos_x && value.pos_y === nextProjectiles[index].pos_y)
          })
        }
        //equalsFigureOpponentBody es true si this.state.figureOpponent === nextFigureOpponent, en caso contrario es false
        let equalsFigureOpponentBody = this.state.figureOpponent["body"].every((value, index) => {
          return (value[0] === nextFigurerOpponent["body"][index][0]
            && value[1] === nextFigurerOpponent["body"][index][1])
        })
        //Esta condicion es para cuando el otro jugador hace una accion y termina con la ronda,
        //sirve para poder actualizar los elementos del tablero al terminar la ronda
        if (this.state.game.turn !== AuthService.getCurrentUser().sub
          && !this.state.finished_round && (!equalsFigureOpponentBody || !equalsProjectiles)) {
          this.setState({
            finished_round: true,
            next_turn: true
          })
        }
      }, 3000);

    } else { clearTimeout(this.timer); }
    if (this.state.finished_round && this.state.game.turn === AuthService.getCurrentUser().sub) {
      //Si es tu turno y finalizaste la ronda
      this.updateRound()
    }
    if (this.state.finished_round && this.state.game.turn !== AuthService.getCurrentUser().sub) {
      //Si no es tu turno pero finalizo la ronda
      this.updateLocalRound()
    }
  }
  shouldComponentUpdate() {
    /**
     * Se hace esto para evitar que cuando quieras elegir una direccion
     * no se ande reiniciando la direccion elegida cada 3 segundos, ya que en
     * componentDidUpdate() se utilizar un timer que provoca que cada 3 segundos
     * se renderice de nuevo el componente*/
    if (this.state.game !== null && !this.state.finished_round && this.state.figure !== null && this.state.figureOpponent !== null
      && this.state.game.turn === AuthService.getCurrentUser().sub && !this.state.next_turn) {
      return false
    } else {
      return true
    }
  }
  /**
   * Dada una accion(disparar o mover) le pega a la API con la correspondiente accion
   * pasada por parametro
   * @param {int} direction una direccion
   * @param {string} action una accion(move o shoot)
   * @param {int} velocity alcance de la accion(solo sirve para la accion mover, o para el proyectil de la artilleria)
   */
  async action(direction, action, velocity) {
    console.log(velocity)
    if (action === "move") {
      let response = await InfantryService.move(this.state.game_id, AuthService.getCurrentUser().sub,
        direction, velocity)
      if (response === "Accion invalida") {
        return alert("Movimiento invalido")
      }
      await this.updateTurn()
      return;
    }
    if (action === "shoot") {
      let response = await InfantryService.shoot(this.state.game_id, AuthService.getCurrentUser().sub,
        direction, 0)
      if (response === "Accion invalida") {
        return alert("Movimiento invalido")
      }
      await this.updateTurn()
      return;
    }
  }

  /**
   * Actualiza el turno, y si acaba la ronda, cambia el estado de finished_round
   */
  async updateTurn() {
    let message = await InfantryService.next_turn(this.state.game_id);
    let data = await InfantryService.getGame(this.state.game_id)

    if (message !== "Ronda terminada") {
      this.setState({
        game: data
      });
    }
    else {
      this.setState({
        game: data,
        finished_round: true
      });
    }
  }

  /**
   * Se utiliza al final de cada ronda cuando es el oponente 
   * quien termino la ronda(en caso contrario utilizar updateRound()),
   * actualiza los proyecttiles y tambien las figuras
   */
  async updateLocalRound() {
    let nextProjectiles = await InfantryService.getProjectile(this.state.game_id)
    let nextFigure = await InfantryService.getFigure(this.state.figure["data"].id_user, this.state.game_id)
    let nextFigureOpponent = await InfantryService.getFigure(this.state.figureOpponent["data"].id_user, this.state.game_id)
    this.setState({
      figure: nextFigure,
      figureOpponent: nextFigureOpponent,
      projectiles: nextProjectiles,
      finished_round: false
    })
  }
  /**
   * Solo se utiliza al final de cada ronda cuando el que termino la ronda
   * fue el jugador de la sesion actual(en otro caso utilizar updateLocalRound()),
   * actualiza los projectiles y tambien las figuras
   */
  async updateRound() {
    //Comienzo a actualizar los proyectiles y figuras en la API
    let is_there_projectiile = ""
    while (is_there_projectiile !== "empty update projectiles queue") {
      is_there_projectiile = await InfantryService.update_projectiles(this.state.game_id)
    }
    let is_there_actions = ""
    while (is_there_actions !== "no actions in queue") {
      is_there_actions = await InfantryService.update_actions(this.state.game_id)

    }
    //Actualizo las figuras y proyectiles en los estados
    let nextFigure = await InfantryService.getFigure(this.state.figure["data"].id_user, this.state.game_id)
    let nextFigureOpponent = await InfantryService.getFigure(this.state.figureOpponent["data"].id_user, this.state.game_id)
    let projectiles = await InfantryService.getProjectile(this.state.game_id)
    this.setState({
      figure: nextFigure,
      figureOpponent: nextFigureOpponent,
      finished_round: false,
      next_turn: false,
      projectiles: projectiles
    })
    this.updateTurn()
  }
  /**
   * Dada la figura actual cuenta la cantidad de casillas que se puede mover
   * @returns devuelve en HTML la cantidad de casillas que se puede mover la figura del jugador
   */
  optionsRender() {
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
    else if (this.state.game.turn === AuthService.getCurrentUser().sub) {
        message = <h3>Your turn</h3>
      }
      else {
        message = (<div>
                      <h3>waiting opponent's turn</h3>
                      <div class="spinner-border" role="status">
                        <span class="sr-only"></span>
                      </div></div>
                  )
      }
    return message
  }


  GameOver() {
    if (this.state.figure !== null && this.state.figureOpponent !== null) {
      console.log(this.state.figure["data"].hp)
      console.log(this.state.figureOpponent["data"].hp)
      if (this.state.figure["data"].hp <= 0 || this.state.figureOpponent["data"].hp <= 0) {
        console.log("Entre")
        
        return true
      } else {
        return false
      }
    }
  }

  render() {
    if (this.state.figure === null || this.state.figureOpponent === null
      || this.state.figure["data"] === undefined || this.state.figureOpponent["data"] === undefined
      || this.state.figure["body"] === undefined || this.state.figureOpponent["body"] === undefined) {
      return (
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
    } else if (this.GameOver()) {
      return (<div class="text-center bg-War">
        <img src={gameOver} />
        <div className="d-flex justify-content-center ">
          
          <p className="display-4 bg-white w-25 rounded-pill p-3">Win Player {this.state.figure["data"].hp <= 0 ? this.state.figure["data"].id_user : 
                                                  this.state.figureOpponent["data"].id_user}</p>
        </div>         
      </div>)

    }
    else {
      return (
        <div>
          <div class="container-fluid bg-War">
            <div class="row align-items-start">
              <div class="col-4 mx-3 mt-5"><FigureInfantryData figure={this.state.figure["data"]} /></div>
              <div> <GameBoard figure={this.state.figure["body"]} figureOpponent={this.state.figureOpponent["body"]} projectiles={this.state.projectiles}/></div>
  
            </div>
            <p class="text-center">{this.getMessageTurn()}</p>
            <div class="row">
          
              <div class="container col">
                {/* Formulario para que el usuario elija que accion desea realizar */}
                <form onSubmit={ev => {
                  ev.preventDefault();
                  this.setState({
                    next_turn: true
                  })
                  this.action(ev.target.direction.value, ev.target.action.value, ev.target.velocity.value)
                }} >
                  {/* botones para seleccionar la direccion */}
                  <br></br>
                  <div class="form-group ">
                    <div class="row justify-content-center">
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

                    <div class="row justify-content-center">
                      <div class="mx-5">
                        <input type="radio" class="btn-check mx-3" name="direction" id="west" autocomplete="off" checked value={WEST} />
                        <label class="btn btn-secondary" for="west">West</label>
                      </div>                      
                      <div className="col-1">

                      </div>
                      <div class="mx-5">
                          
                        <label class="btn btn-secondary" for="east">East</label>
                        <input type="radio" class="btn-check mx-3" name="direction" id="east" autocomplete="off" checked value={EAST} />
                      </div>
                        
                      
                    </div>

                    <div class="row justify-content-center">
                      <div>
                        <label class="btn btn-secondary col" for="south west" >South west</label>
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
                  <br></br>
                  <div className="row justify-content-center">
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
                  </div>
                  <br></br><br></br><br></br>
                  <div class="text-center position-absolute top-50 start-50 translate-middle col">
                    <button type="submit" class="btn btn-outline-light" disabled={this.state.finished_round || this.state.game.turn !== AuthService.getCurrentUser().sub}>Next turn</button>
                  </div>
                </form>
              </div>
              
            </div>
            <div>

            </div>
          </div>
        </div>
      )
    }
  }
}