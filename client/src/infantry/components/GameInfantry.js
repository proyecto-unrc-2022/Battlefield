import React, { Component } from "react";
import TableGame from "./tableGame.component";
import FigureInfantryData from "./figureInfantryInfo.component";
import "./FigureData.css";

// const renderTable = () => {
//   for (let i = 0; i < 10; i++) {
//     <ul></ul>;
//     for (let j = 0; i < 20; j++) {
//       <li className="square"></li>;
//     }
//   }
//};
export default class GameInfantry extends Component {
  constructor(props) {
    super(props);

    this.state = {
      content: null,
    };
  }

  render() {
    return (
      <div>
        {/*
         <FigureInfantryData game_id={1} user_id={1}/>
         Agrego valores fijos para poder testear
         */}
        <div className="jugador1"><FigureInfantryData game_id={1} user_id={1} /></div>
        <div className="jugador2"><FigureInfantryData game_id={1} user_id={2} /></div>
        <TableGame>
        </TableGame>
        
        
      </div>
    )
  }
}
