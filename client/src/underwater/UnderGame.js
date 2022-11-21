import React from "react";
import { useState, useEffect } from "react";
import { useParams } from "react-router-dom";
import ChooseSubmarine from "./ChooseSubmarine";
import PlaceSubmarine from "./PlaceSubmarine";
import UnderBoard from "./UnderBoard";
import "./css/style.css"
import "./css/game-style.css"

export default function UnderGame() {
  const params = useParams();
  const [chosenSubmarine, setChosenSubmarine] = useState(null);
  const [subWasPlaced, setSubWasPlaced] = useState(false);
  const [layout, setLayout] = useState(null);

  useEffect(() => {
    if(chosenSubmarine != null) {
      if(subWasPlaced)
        setLayout({main: <UnderBoard id={params.id} width={20} height={10} />, bottom: <span>Acá van los controles</span>});
      else
        setLayout({main: <PlaceSubmarine setSubWasPlaced={setSubWasPlaced} />, bottom: <h1>Place your submarine</h1>});
    } else
      setLayout({main: <ChooseSubmarine setChosenSubmarine={setChosenSubmarine} />, bottom: <h1>Choose your fighter</h1>});
  }, [chosenSubmarine, subWasPlaced]);

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
