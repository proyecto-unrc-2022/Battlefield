import React, { useState, useEffect } from "react";
import "./css/game-style.css"
import UnderCell from "./UnderCell";

export default function PlaceSubmarine(props) {
  const [cells, setCells] = useState([]);

  useEffect(() => {
    let cells = []
    for(let i = 0; i < props.height; i++) {
      cells.push([]);
      for(let j = 0; j < props.width; j++){
        cells[i].push("" + (i+1) + "," + (j+1));
      }
    }
    setCells(cells);
  }, []);

  function placeSubmarine(x,y) {
    let dir = y < props.width/2 ? 2 : 6;
    props.setPosition({x: x, y: y, direction: dir});
  }

  return (
    <div className={"u-grid-" + props.width}>
      {cells.map((row, i) => {
        return row.map((_, j) => {
          return (<UnderCell placeSubmarine={placeSubmarine} key={(i+1)*(j+1)} x={i} y={j} className="u-cell" type="" images={null} />);
        })
      })}
    </div>
  );
}
