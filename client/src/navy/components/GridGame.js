import React from "react";
import ShipService from "../services/ShipService";
import CellGameBoard from "./CellGameBoard";
import "./GridGame.css";
import WaterWave from "react-water-wave";
import sea from "../assets/sea.jpg";

const GridGame = ({
  rows,
  cols,
  myShip,
  enemyShip,
  missiles,
  selectMissile,
}) => {
  const arr = Array(rows).fill(Array(cols).fill(1));
  console.log(enemyShip);

  const visibleCell = (row, col) => {
    return (
      row <= myShip.x + 5 &&
      row >= myShip.x - 5 &&
      col <= myShip.y + 5 &&
      col >= myShip.y - 5
    );
  };

  const getEntity = (row, col) => {
    const posMyShip = ShipService.buildShip(myShip);
    let entity = null;
    posMyShip.forEach((pos) => {
      if (row === pos.x && col === pos.y) {
        entity = { ...pos, type: "my-ship" };
      }
    });

    if (enemyShip !== null) {
      const posEnemyShip = ShipService.buildShip(enemyShip);
      posEnemyShip.forEach((pos) => {
        if (row === pos.x && col === pos.y) {
          entity = { ...pos, type: "enemy-ship" };
        }
      });
    }

    missiles.forEach((missile) => {
      if (row === missile.pos_x && col === missile.pos_y) {
        entity = { ...missile, type: "missile" };
      }
    });

    return entity;
  };

  return (
    <div className="d-flex">
      <WaterWave
        className="image"
        imageUrl={sea}
        perturbance={0.005}
        resolution={256}
        dropRadius={30}
      >
        {(play) => (
          <div className="grid-game">
            {arr.map((el, row) => {
              return el.map((elem, col) => {
                return (
                  <CellGameBoard
                    key={row * 20 + (col + 1)}
                    visible={visibleCell(row + 1, col + 1)}
                    col={col + 1}
                    row={row + 1}
                    entity={getEntity(row + 1, col + 1)}
                    selectMissile={(entity) => selectMissile(entity)}
                  />
                );
              });
            })}
          </div>
        )}
      </WaterWave>
    </div>
  );
};

export default GridGame;
