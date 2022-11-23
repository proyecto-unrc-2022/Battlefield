import axios from 'axios';
import React, {useEffect, useState} from 'react'; 
import "./css/game-style.css"
import authHeader from "../services/auth-header"
import UnderCell from './UnderCell';

const baseURL = "http://127.0.0.1:5000/api/v1/underwater";


export default function UnderBoard({board, height, width}) {
  const images = {
    "FH": require("./css/FH.png"),
    "FT": require("./css/FT.png"),
  };

  useEffect(_ => console.log("Board updated", board), [board])

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
