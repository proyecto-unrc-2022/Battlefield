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
  selected,
}) => {
  return (
    <div
      onMouseEnter={() => handleMouseEnter(row, col, index)}
      onMouseLeave={() => handleMouseLeave()}
      className={
        "cell " +
        (hovered ? "hovered " : "") +
        (invalid ? "invalid " : "") +
        (selected ? "selected-cell " : "")
      }
      onClick={() => action(row, col)}
    ></div>
  );
};

export default CellShipPlace;
