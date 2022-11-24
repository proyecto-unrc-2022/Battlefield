import React, { useState } from 'react'
import "./GridShipPlace.css"
import CellShipPlace from "./CellShipPlace"

const GridShipPlace = ({course, size, rows, cols, selectPosition}) => {
  const arr = Array(rows).fill(Array(cols / 2).fill(1));

  const [hovered, setHovered] = useState([]);
  const [invalids, setInvalids] = useState([]);

  const rowAndColtoIndex = (row, col) => (row * 10) + (col + 1);

  const compass = {
    N: { x: -1, y: 0 },
    S: { x: 1, y: 0 },
    E: { x: 0, y: 1 },
    W: { x: 0, y: -1 },
    NE: { x: -1, y: 1 },
    NW: { x: -1, y: -1 },
    SE: { x: 1, y: 1 },
    SW: { x: 1, y: -1 },
  };

  const inverseCoords = {
    N: "S",
    S: "N",
    W: "E",
    E: "W",
    SE: "NW",
    NW: "SE",
    SW: "NE",
    NE: "SW",
  };

  const outOfRange = (row, col) => {
    return row < 1 || row > 10 || col < 1 || col > 10;
  };

  const handleMouseEnter = (row, col, index) => {
    const hovered = [index];
    let invalid = false;
    for (let i = 0; i < size - 1 && !invalid; i++) {
      row = row + compass[inverseCoords[course]].x;
      col = col + compass[inverseCoords[course]].y;
      if (outOfRange(row, col)) {
        invalid = true;
      } else {
        hovered.push((row - 1) * 10 + col);
      }
    }
    if (invalid) {
      setInvalids(hovered);
    } else {
      setHovered(hovered);
    }
  };

  const handleMouseLeave = () => {
    setHovered([]);
    setInvalids([]);
  };

  const handleCellClick = (row, col) => {
    let invalid = false;
    let newRow = row;
    let newCol = col;
    for (let i = 0; i < size - 1 && !invalid; i++) {
      newRow = newRow + compass[inverseCoords[course]].x;
      newCol = newCol + compass[inverseCoords[course]].y;
      if (outOfRange(newRow, newCol)) {
        invalid = true;
      }
    }
    if (!invalid) {
      selectPosition(row, col);
    }
  };

  return (
    <div className='grid'>
      {arr.map((el, row) => {
        return el.map((elem, col) => {
          return (
            <CellShipPlace
              key={rowAndColtoIndex(row, col)}
              index={rowAndColtoIndex(row, col)}
              row={row + 1}
              col={col + 1}
              handleMouseEnter={handleMouseEnter}
              handleMouseLeave={handleMouseLeave}
              action={handleCellClick}
              hovered={hovered.includes(rowAndColtoIndex(row, col))}
              invalid={invalids.includes(rowAndColtoIndex(row, col))}
            />
          );
        });
      })}
    </div>
  )
}

export default GridShipPlace