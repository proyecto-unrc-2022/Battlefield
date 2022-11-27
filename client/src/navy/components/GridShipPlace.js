import React, { useState } from "react";
import "./GridShipPlace.css";
import CellShipPlace from "./CellShipPlace";
import ShipService from "../services/ShipService";
import WaterWave from "react-water-wave";
import sea from "../assets/sea.jpg";

const GridShipPlace = ({ course, size, rows, cols, selectPosition }) => {
  const arr = Array(rows).fill(Array(cols / 2).fill(1));

  const [hovered, setHovered] = useState([]);
  const [invalids, setInvalids] = useState([]);
  const [selectedPositions, setSelectedPositions] = useState([]);

  const rowAndColtoIndex = (row, col) => row * 10 + (col + 1);

  const handleMouseEnter = (row, col, index) => {
    const hovered = [index];
    let invalid = false;
    for (let i = 0; i < size - 1 && !invalid; i++) {
      row = row + ShipService.compass[ShipService.inverseCoords[course]].x;
      col = col + ShipService.compass[ShipService.inverseCoords[course]].y;
      if (ShipService.outOfRange(row, col)) {
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
    const selected = [(row - 1) * 10 + col];
    let invalid = false;
    let newRow = row;
    let newCol = col;
    for (let i = 0; i < size - 1 && !invalid; i++) {
      newRow =
        newRow + ShipService.compass[ShipService.inverseCoords[course]].x;
      newCol =
        newCol + ShipService.compass[ShipService.inverseCoords[course]].y;
      if (ShipService.outOfRange(newRow, newCol)) {
        invalid = true;
      } else {
        selected.push((newRow - 1) * 10 + newCol);
      }
    }
    if (!invalid) {
      setSelectedPositions(selected);
      selectPosition(row, col);
    }
  };

  return (
    <WaterWave
      className="image mx-auto"
      imageUrl={sea}
      perturbance={0.005}
      resolution={256}
      dropRadius={30}
    >
      {(play) => (
        <div className="grid-ship-place">
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
                  selected={selectedPositions.includes(
                    rowAndColtoIndex(row, col)
                  )}
                />
              );
            });
          })}
        </div>
      )}
    </WaterWave>
  );
};

export default GridShipPlace;
