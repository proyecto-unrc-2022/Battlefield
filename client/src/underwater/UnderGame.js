import React from "react";
import { useState, useEffect, useRef } from "react";
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
  const sessionId = params.id;
  const [chosenSubmarine, setChosenSubmarine] = useState(null);
  const [position, setPosition] = useState(null);
  const [layout, setLayout] = useState(null);
  const requestWasSent = useRef(false);
  const [visibleState, setVisibleState] = useState(null);
  const URL = "http://localhost:5000/api/v1/underwater/game/" + sessionId;


  function sendChooseSubmarine() {
    const headers = authHeader();
    headers["Content-Type"] = "application/json";
    axios.post(
      URL + "/choose_submarine",
      {
        submarine_id: chosenSubmarine,
        x_position: position.x,
        y_position: position.y,
        direction: position.direction
      },
      { headers: headers }
    ).then(_ => {console.log("Submarine chosen"); updateVisibleState()});
  }

  function updateVisibleState() {
    axios.get(
      URL,
      {headers: authHeader()}
    ).then(response => {
      console.log("Setting visible state", response.data);
      setVisibleState(response.data);
    })
  }

  useEffect(_ => {
    if(chosenSubmarine != null) {
      if(position != null) {
        if(!requestWasSent.current) {
          sendChooseSubmarine();
          requestWasSent.current = true;
        }
        setLayout({
          main: <UnderBoard visibleState={visibleState} width={width} height={height} />,
          bottom: <UnderControls visibleState={visibleState} updateVisibleState={updateVisibleState} position={position} setPosition={setPosition}/>
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
  }, [chosenSubmarine, position, visibleState]);

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
