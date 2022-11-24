import React, {useEffect, useState} from 'react'; 
import "./css/game-style.css"
import UnderCell from './UnderCell';

const baseURL = "http://127.0.0.1:5000/api/v1/underwater";


export default function UnderBoard({visibleState, height, width}) {
  const [board, setBoard] = useState([]);
  const images = {
    "FH": require("./css/FH.png"),
    "FT": require("./css/FT.png"),
  };

  function getVisibility() {
    const visibility = visibleState.visible_board;
    const cells = []
    for (let i = 0; i < height; i++) {
      cells.push([])
      for (let j = 0; j < width; j++) {
        if (visibility[i] === undefined) {
          cells[i].push("nv");
        } else {
          let visibility_i = visibility[i]
          if (visibility_i[j] === undefined) {
            cells[i].push("nv");
          } else {
            cells[i].push(visibility[i][j]);
          }
        }
      }
    }
    console.log("Updating board", cells);
    setBoard(cells);
  }

  useEffect(_ => {if(visibleState != null) {getVisibility()}}, [visibleState]);

  return (
    <div className={"u-grid-" + width}>
      {
        board.map((row, i) =>{
          return row.map((col, j) => {
            return (<UnderCell key={(i+1)*(j+1)} type={col} images={images} />);
          })
        })
      }
    </div>
  )
}
