import axios from 'axios';
import React, {useEffect, useState} from 'react'; 
import "./css/game-style.css"
import authHeader from "../services/auth-header"
import UnderCell from './UnderCell';

const baseURL = "http://127.0.0.1:5000/api/v1/underwater";


export default function UnderBoard({id, height, width}) {
  const [board, setBoard] = useState([]);
  const images = {
    "FH": require("./css/FH.png"),
    "FT": require("./css/FT.png"),
  };

  function getVisibility() {
    axios.get(
      baseURL + "/game/" + id,
      {headers: authHeader()}
    ).then(response => {
      console.log(response.data.visible_board);
      let visibility = response.data.visible_board;
      let cells = []
      for(let i = 0; i<height; i++){
        cells.push([])
        for (let j = 0; j< width; j++){
          if(visibility[i] === undefined){
            cells[i].push("nv");
          }else{
            let visibility_i = visibility[i]
            if(visibility_i[j] === undefined){
              cells[i].push("nv");
            }else{
              cells[i].push(visibility[i][j]);
            }
          }
        }
      }
      setBoard(cells);
    }).catch(error => {console.log(error)})
  }

  useEffect(() =>{
    getVisibility();
  }, []);

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
