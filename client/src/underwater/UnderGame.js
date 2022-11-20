import React from "react";
import { useState } from "react";
import ChooseSubmarine from "./ChooseSubmarine";
import "./css/style.css"

export default function UnderGame() {
  const [subWasChosen, setWasSubChosen] = useState(false);

  return (
    <div className="u-container">
    {subWasChosen ? null : <ChooseSubmarine />}
    </div>
  );
}
