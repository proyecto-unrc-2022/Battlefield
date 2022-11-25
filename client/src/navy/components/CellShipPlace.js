import React from "react";
import "./CellShipPlace.css";

const CellShipPlace = ({
  row,
  col,
  index,
  handleMouseEnter,
  hovered,
  invalid,
  handleMouseLeave,
  action,
}) => {
  return (
    <div
      onMouseEnter={() => handleMouseEnter(row, col, index)}
      onMouseLeave={() => handleMouseLeave()}
      className={
        "cell " + (hovered ? "hovered" : "") + (invalid ? "invalid" : "")
      }
      onClick={() => action(row, col)}
    ></div>
  );
};

export default CellShipPlace;
