import React from "react";
import { useState, useEffect } from "react";
import { useParams } from "react-router-dom";
import axios from "axios";
import authHeader from "../services/auth-header";
import ChooseSubmarine from "./ChooseSubmarine";
import PlaceSubmarine from "./PlaceSubmarine";
import UnderBoard from "./UnderBoard";
import UnderControls from "./UnderControls";
import "./css/style.css"
import "./css/game-style.css"

export default function UnderGame() {
  const params = useParams();
  const width = 20;
  const height = 10;
  const [chosenSubmarine, setChosenSubmarine] = useState(null);
  const [position, setPosition] = useState(null);
  const [layout, setLayout] = useState(null);
  const URL = "http://localhost:5000/api/v1/underwater/game/" + params.id;

  function sendChooseSubmarine() {
    const headers = authHeader();
    headers["Content-Type"] = "multipart/form-data";
    axios.post(
      URL + "/choose_submarine",
      {
        submarine_id: chosenSubmarine,
        x_position: position.x,
        y_position: position.y,
        direction: position.direction
      },
      { headers: headers }
    )
  }

  useEffect(() => {
    if(chosenSubmarine != null) {
      if(position != null) {
        sendChooseSubmarine();
        setLayout({
          main: <UnderBoard id={params.id} width={width} height={height} />,
          bottom: <UnderControls />
        });
      }
      else
        setLayout({
          main: <PlaceSubmarine setPosition={setPosition} width={width} height={height} />, 
          bottom: <h1>Place your submarine</h1>
        });
    } else
      setLayout({
        main: <ChooseSubmarine setChosenSubmarine={setChosenSubmarine} />,
        bottom: <h1>Choose your fighter</h1>
      });
  }, [chosenSubmarine, position]);

  return (
    <div className="u-container">
      <div className="u-game-container">
        <div className="u-screen">
          {layout == null ? null : layout.main}
        </div>
        <div className="u-bottom-div">
          {layout == null ? null : layout.bottom}
        </div>
      </div>
    </div>
  );
}
