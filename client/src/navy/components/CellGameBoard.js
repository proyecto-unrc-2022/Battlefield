import React from "react";
import "./CellGameBoard.css";
import missile from "../assets/missile.png";

const CellGameBoard = ({ visible, col, row, entity, selectMissile }) => {
  return (
    <>
      {!visible ? (
        <div className="cell-game not-visible"></div>
      ) : entity?.type === "missile" ? (
        <div
          role={"button"}
          onClick={() => selectMissile(entity)}
          className="cell-game"
        >
          <img
            className={"h-auto " + entity.course}
            src={missile}
            alt={"Missile"}
          ></img>
        </div>
      ) : entity?.type === "enemy-ship" ? (
        <div className={"cell-game " + entity.course}>
          <div className={"enemy " + (entity.proa ? "proa" : "")}></div>
        </div>
      ) : entity?.type === "my-ship" ? (
        <div className={"cell-game " + entity.course}>
          <div className={"my-ship " + (entity.proa ? "proa" : "")}></div>
        </div>
      ) : (
        <div className="cell-game"></div>
      )}
    </>
  );
};

export default CellGameBoard;
