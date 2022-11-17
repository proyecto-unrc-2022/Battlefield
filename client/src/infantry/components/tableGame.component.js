import React, { Component } from "react";
import "./TableGames.css";
import InfantryService from "../services/infantry.service"

const FIGURE = 1
const PROJECTILE = 2


let table = (new Array(10)).fill().map(function(){ return new Array(20).fill(0);});
export default class TableGame extends Component {
  constructor(props) {
    super(props);
    this.state = {
      figure1: null,
      figure2: null,
      projectiles: null
    }
  }

  async componentDidMount(){
    const f1 = await InfantryService.getFigure(1, 1)
    const f2 = await InfantryService.getFigure(2, 1)
    const projectiles = await InfantryService.getProjectile(1)
    this.setState({
      figure1 : f1["body"],
      figure2 : f2["body"],
      projectiles: projectiles
    })
    
  }

  render() {
    const casillas = [];
    if (this.state.figure1 != null && this.state.figure2 != null){
      this.state.figure1.map(coor => table[coor[1]][coor[0]] = FIGURE)
      this.state.figure2.map(coor => table[coor[1]][coor[0]] = FIGURE)
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