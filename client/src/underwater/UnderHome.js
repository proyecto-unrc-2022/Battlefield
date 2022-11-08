import React from "react";
import { Link } from "react-router-dom";
import "./css/style.css"

function UnderHome() {
  return (
    <div className="u-container">
      <div className="u-title">Battle Submarine</div>
      <div className="u-options">
        <Link style={{textDecoration: 'none'}} to={"/under-new-game"}><div className="u-big-button">New Game</div></Link>
        <Link style={{textDecoration: 'none'}} to={"/under-join-game"}><div className="u-big-button">Join Game</div></Link>
      </div>
    </div>
  );
}

export default UnderHome;
