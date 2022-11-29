import React, { Component, useEffect } from "react";
import "./TableGames.css";
import InfantryService from "../services/infantry.service"

const FIGURE = 1
const FIGUREOPPONENT = 11
const PROJECTILE = 2


/**
 * Renderiza el tablero del juego junto a las figuras y projectiles que se pasan por parametros
 */

export default class GameBoard extends Component {
  constructor(props) {
    super(props);
    this.state = {
      figure: props.figure,
      figureOpponent: props.figureOpponent,
      projectiles: props.projectiles
    }
  }
  //Actualiza el estado de las figuras y los projectiles
  componentDidUpdate(prevProps) {
    if (prevProps.figure !== this.props.figure || prevProps.figureOpponent !== this.props.figureOpponent
      || prevProps.projectiles !== this.props.projectiles) {
      this.setState({
        figure: this.props.figure,
        figureOpponent: this.props.figureOpponent,
        projectiles: this.props.projectiles
      })
    }
  }

  /**
  * Verifica si las coordenadas estan dentro del mapa
  * @param {Array} coor coordenadas
  * @returns True si las coordenadas estan dentro del mapa, False en caso contrario
  */
  is_it_on_map(coor) {
    if (coor[0] >= 0 && coor[0] < 20 && coor[1] >= 0 && coor[1] < 10) {
      return true
    }
    return false
  }

  /**
   * Dado a los estados actuales del componente, dibuja el tablero del juego 
   * representado por un arreglo y tambien las figuras y projectiles, 0 representando una casilla terrestre
   * @returns Tablero del juego con los datos del estado actual del componente
   */
  drawGameBoard() {
    let board = (new Array(10)).fill().map(function () { return new Array(20).fill(0); });
    this.state.figure["body"].map(coor => { if (this.is_it_on_map(coor)) { board[coor[1]][coor[0]] = FIGURE } })
    this.state.figureOpponent["body"].map(coor => { if (this.is_it_on_map(coor)) { board[coor[1]][coor[0]] = FIGUREOPPONENT } })
    if (this.state.projectiles !== undefined) {
      this.state.projectiles.map( (projectile) => {if(board[projectile["pos_y"]][projectile["pos_x"]] !== FIGURE &&
      board[projectile["pos_y"]][projectile["pos_x"]] !== FIGUREOPPONENT) board[projectile["pos_y"]][projectile["pos_x"]] = PROJECTILE})
    }

    return board
  }

  render() {

    let board = this.drawGameBoard()

    const casillas = [];

    let cabX = this.state.figure["body"][0][1]
    let cabY = this.state.figure["body"][0][0]

    console.log(cabX)
    console.log(cabY)

    for (let i = 0; i < board.length; i++) {
      const mapItem = [];
      for (let j = 0; j < board[i].length; j++) {

        

        if (board[i][j] === 11 && (board[i][j + 2] === 1 ||
          board[i][j + 1] === 1 ||
          board[i][j - 2] === 1 ||
          board[i][j - 1] === 1 ||
          i > 0 && board[i - 1][j] === 1 ||
          i > 1 && board[i - 2][j] === 1 ||
          i < 7 && board[i + 2][j] === 1 ||
          i < 8 && board[i + 1][j] === 1 ||
          i < 8 && board[i + 1][j - 1] === 1 ||
          i < 8 && board[i + 1][j + 1] === 1 ||
          i > 0 && board[i - 1][j + 1] === 1 ||
          i > 0 && board[i - 1][j - 1] === 1 
           )) {
          mapItem.push(<li class="square p-3 bg-warning"></li>);
        }
        else if (board[i][j] === PROJECTILE && (board[i][j + 2] === 1 ||
          board[i][j + 1] === 1 ||
          board[i][j - 2] === 1 ||
          board[i][j - 1] === 1 ||
          i > 0 && board[i - 1][j] === 1 ||
          i > 1 && board[i - 2][j] === 1 ||
          i < 7 && board[i + 2][j] === 1 ||
          i < 8 && board[i + 1][j] === 1 ||
          i < 8 && board[i + 1][j - 1] === 1 ||
          i < 8 && board[i + 1][j + 1] === 1 ||
          i > 0 && board[i - 1][j + 1] === 1 ||
          i > 0 && board[i - 1][j - 1] === 1 
        )) {
          mapItem.push(<li class="square p-3 bg-danger"></li>);
        }

        else if(i === cabX && j === cabY){
          if(board[i][j] === 1){
            mapItem.push(<li class="square p-3 bg-info"></li>);
          }
        }

        

        else if (board[i][j] === 1 ) {
          mapItem.push(<li class="square p-3 bg-primary"></li>);
        }

        else if (board[i][j + 2] === 1 ) {
          mapItem.push(<li class="square p-3 bg-white"></li>);
        }
        else if (board[i][j + 1] === 1 ) {
          mapItem.push(<li class="square p-3 bg-white"></li>);
        }
        else if (board[i][j - 2] === 1 ) {
          mapItem.push(<li class="square p-3 bg-white"></li>);
        }
        else if (board[i][j - 1] === 1 ) {
          mapItem.push(<li class="square p-3 bg-white"></li>);
        }
        else if (i > 0 && board[i - 1][j] === 1 ) {
          mapItem.push(<li class="square p-3 bg-white"></li>);
        }
        else if (i > 1 && board[i - 2][j] === 1 ) {
          mapItem.push(<li class="square p-3 bg-white"></li>);
        }
        else if (i < 7 && board[i + 2][j] === 1 ) {
          mapItem.push(<li class="square p-3 bg-white"></li>);
        }
        else if (i < 8 && board[i + 1][j] === 1 ) {
          mapItem.push(<li class="square p-3 bg-white"></li>);
        }
        else if (i < 8 && board[i + 1][j - 1] === 1 ) {
          mapItem.push(<li class="square p-3 bg-white"></li>);
        }
        else if (i < 8 && board[i + 1][j + 1] === 1 ) {
          mapItem.push(<li class="square p-3 bg-white"></li>);
        }
        else if (i > 0 && board[i - 1][j + 1] === 1 ) {
          mapItem.push(<li class="square p-3 bg-white"></li>);
        }
        else if (i > 0 && board[i - 1][j - 1] === 1 ) {
          mapItem.push(<li class="square p-3 bg-white"></li>);
        }
        
        else {
          mapItem.push(<li class="square p-3"></li>);
        }
      }
      casillas.push(<ul class="list-unstyled">{mapItem}</ul>);
    }

    return casillas;



  }
}