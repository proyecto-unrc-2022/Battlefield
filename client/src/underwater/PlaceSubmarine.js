import React, { useState, useEffect } from "react";
import "./css/game-style.css";
import AuthService from "../services/auth.service";
import UnderCell from "./UnderCell";

export default function PlaceSubmarine(props) {
  const { visibleState, setPosition, width, height } = props;
  const currentUserId = AuthService.getCurrentUser().sub;
  const [cells, setCells] = useState([]);

  useEffect(() => {
    const cells = [];
    for (let i = 0; i < height; i++) {
      cells.push([]);
      for (let j = 0; j < width; j++) {
        cells[i].push(`${i + 1},${j + 1}`);
      }
    }
    setCells(cells);
  }, [height, width]);

  function placeSubmarine(x, y) {
    const dir = y < width / 2 ? 2 : 6;
    setPosition({ x, y, direction: dir });
  }

  return (
    <div style={{ height: `${976 / 2}px` }} className={`u-grid-${width}`}>
      {cells.map((row, i) =>
        row.map((_, j) => {
          if (visibleState.host_id === currentUserId) {
            if (j < width / 2) {
              return (
                <UnderCell
                  placeSubmarine={placeSubmarine}
                  key={(i + 1) * (j + 1)}
                  x={i}
                  y={j}
                  className="u-cell"
                  typeString=""
                  images={null}
                />
              );
            }
            return (
              <UnderCell
                key={(i + 1) * (j + 1)}
                x={i}
                y={j}
                className="u-cell"
                typeString="nv"
                images={null}
              />
            );
          }
          if (visibleState.visitor_id === currentUserId) {
            if (j < width / 2) {
              return (
                <UnderCell
                  key={(i + 1) * (j + 1)}
                  x={i}
                  y={j}
                  className="u-cell"
                  typeString="nv"
                  images={null}
                />
              );
            }
            return (
              <UnderCell
                placeSubmarine={placeSubmarine}
                key={(i + 1) * (j + 1)}
                x={i}
                y={j}
                className="u-cell"
                typeString=""
                images={null}
              />
            );
          }
        })
      )}
    </div>
  );
}
