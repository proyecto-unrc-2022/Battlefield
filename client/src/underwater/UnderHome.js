import React, { useState } from "react";
import "./css/style.css"
import UnderNewGame from "./UnderNewGame";
import HomeButtons from "./UnderHomeButtons";
import JoinGame from "./UnderJoinGame";

export default function UnderHome() {
  const [visibleComp, setVisibleComp] = useState("home");

  function selectComponent(visibleComp) {
    switch (visibleComp) {
      case "home":
        return <HomeButtons setVisibleComp={setVisibleComp} />;
      case "new":
        return <UnderNewGame setVisibleComp={setVisibleComp} />;
      case "join":
        return <JoinGame setVisibleComp={setVisibleComp} />;
      default:
        return null;
    }
  }

  return (
    <div className="u-container">
      <div className="u-title">SUBMARINE BATTLE</div>
      {selectComponent(visibleComp)}
    </div>
  );
}
