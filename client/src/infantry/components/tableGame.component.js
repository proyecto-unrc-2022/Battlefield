import React, { Component, useEffect } from "react";
import "./TableGames.css";
import InfantryService from "../services/infantry.service"

const FIGURE = 1
const PROJECTILE = 2


export default class TableGame extends Component {
  constructor(props) {
    super(props);
    this.state = {
      game_id: props.game_id,
      player1_id: props.player1_id,
      player2_id: props.player2_id,
      figure1: null,
      figure2: null,
      projectiles: null
    }
  }

  async componentDidMount(){
    const f1 = await InfantryService.getFigure(this.state.player1_id, this.state.game_id)
    const f2 = await InfantryService.getFigure(this.state.player2_id, this.state.game_id)
    const projectiles = await InfantryService.getProjectile(this.state.game_id)
    this.setState({
      figure1 : f1["body"],
      figure2 : f2["body"],
      projectiles: projectiles
    }) 
  }
  async componentDidUpdate(prevProps, prevState){
    const f1 = await InfantryService.getFigure(this.state.player1_id, this.state.game_id)
    const f2 = await InfantryService.getFigure(this.state.player2_id, this.state.game_id)
    const projectiles = await InfantryService.getProjectile(1)
    if(prevState.figure1 !== f1["body"] || prevState.figure2 !== f2["body"]
    || prevState.projectiles !== projectiles){
      this.setState({
        figure1 : f1["body"],
        figure2 : f2["body"],
        projectiles: projectiles
      }) 
    }
  }
  is_it_on_map(coor){
    if(coor[0] >= 0 && coor[0] < 20 && coor[1] >= 0 && coor[1] < 10){
      return true
    }
    return false
  }

  render() {
    let table = (new Array(10)).fill().map(function(){ return new Array(20).fill(0);});
    const casillas = [];
    if (this.state.figure1 != null && this.state.figure2 != null){
      this.state.figure1.map(coor => {if(this.is_it_on_map(coor)){table[coor[1]][coor[0]] = FIGURE}})
      this.state.figure2.map(coor => {if(this.is_it_on_map(coor)){table[coor[1]][coor[0]] = FIGURE}})
    }
    if(this.state.projectiles !=null){
      this.state.projectiles.map(projectile => table[projectile["pos_y"]][projectile["pos_x"]] = PROJECTILE)
    }
    for (let i = 0; i < table.length; i++) {
      const mapItem = [];
      for (let j = 0; j < table[i].length; j++) {

        if(table[i][j] === 1){
          mapItem.push(<li class="square p-3 bg-dark"></li>);
        }
        else if(table[i][j] === PROJECTILE){
          mapItem.push(<li class="square p-3 bg-danger"></li>);
        }
        else{
          mapItem.push(<li class="square p-3"></li>);
        }
        
      }
      casillas.push(<ul class="list-unstyled">{mapItem}</ul>);
    }
    return casillas;
  }
}