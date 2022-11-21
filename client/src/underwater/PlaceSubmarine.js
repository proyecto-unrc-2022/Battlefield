import React, { useState, useEffect } from "react";
import "./css/game-style.css"

export default function PlaceSubmarine({setSubWasPlaced}) {
  const [cells, setCells] = useState([]);

  useEffect(() => {
    let cells = []
    for(let i = 0; i < 10; i++) {
      cells.push([]);
      for(let j = 0; j < 20; j++){
        cells[i].push("" + (i+1) + "," + (j+1));
      }
    }
    setCells(cells);
  }, []);

  function onClick() {
    setSubWasPlaced(true);
  }

  return (
    <div className="u-grid">
      {cells.map((row, i) => {
        return row.map((col, j) => {
          return <div onClick={onClick} key={(i+1)*(j+1)} className="u-cell">{col}</div>
        })
      })}
    </div>
  );
}
