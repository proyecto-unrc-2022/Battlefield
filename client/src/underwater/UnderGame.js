import React from "react";
import { useState, useEffect } from "react";
import ChooseSubmarine from "./ChooseSubmarine";
import "./css/style.css"
import "./css/game-style.css"

export default function UnderGame() {
  const [subWasChosen, setSubWasChosen] = useState(false);
  const [subWasPlaced, setSubWasPlaced] = useState(false);
  const [layout, setLayout] = useState(null);

  useEffect(() => {
    if(subWasChosen) {
      if(subWasPlaced)
        setLayout({main: null, bottom: null});
      else
        setLayout({main: null, bottom: null});
    } else
      setLayout({main: <ChooseSubmarine />, bottom: <h1>Choose your fighter</h1>});
  }, [subWasChosen, subWasPlaced]);

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
