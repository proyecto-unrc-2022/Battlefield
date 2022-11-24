import React, { useEffect, useState } from "react";
import "./CellGameBoard.css";

const CellGameBoard = ({ visible, col, row, entity, selectMissile }) => {

  return (
    <>
      {(!visible) ? (
        <div className="cell-game not-visible"></div>
      ) : ((entity?.type === "missile") ? (
        <div onClick={() => selectMissile(entity)} className="cell-game">M</div>
      ) : ((entity?.type === "enemy-ship") ? (
        <div className="cell-game">E</div>
      ) : ((entity?.type === "my-ship") ? (
        <div className="cell-game">S</div>
      ) : (
        <div className="cell-game"></div>
      ))))}
    </>
  );
};

export default CellGameBoard;
