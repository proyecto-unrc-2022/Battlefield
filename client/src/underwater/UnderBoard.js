import React, { useEffect, useState } from "react";
import "./css/game-style.css";
import UnderCell from "./UnderCell";

export default function UnderBoard({ visibleState, height, width }) {
  const [board, setBoard] = useState([]);
  const images = {
    Saukko: {
      F: {
        H: require("./css/submarineimages/submarine0HeadF.png"),
        T: require("./css/submarineimages/submarine0TailF.png"),
      },
      E: {
        H: require("./css/submarineimages/submarine0HeadE.png"),
        T: require("./css/submarineimages/submarine0TailE.png"),
      },
    },
    Nautilus: {
      F: {
        H: require("./css/submarineimages/submarine1HeadF.png"),
        T: require("./css/submarineimages/submarine1TailF.png"),
      },
      E: {
        H: require("./css/submarineimages/submarine1HeadE.png"),
        T: require("./css/submarineimages/submarine1TailE.png"),
      },
    },
    "USS Sturgeon": {
      F: {
        H: require("./css/submarineimages/submarine2HeadF.png"),
        T: require("./css/submarineimages/submarine2TailF.png"),
      },
      E: {
        H: require("./css/submarineimages/submarine2HeadE.png"),
        T: require("./css/submarineimages/submarine2TailE.png"),
      },
    },
    Surcouf: {
      F: {
        H: require("./css/submarineimages/submarine3HeadF.png"),
        T: require("./css/submarineimages/submarine3TailF.png"),
      },
      E: {
        H: require("./css/submarineimages/submarine3HeadE.png"),
        T: require("./css/submarineimages/submarine3TailE.png"),
      },
    },
    Torpedo: {
      F: {
        "*": require("./css/images/torpedoF.png"),
      },
      E: {
        "*": require("./css/images/torpedoE.png"),
      },
    },
  };

  function getVisibility() {
    if (visibleState === null || visibleState.visible_board === undefined)
      return;
    const visibility = visibleState.visible_board;
    const cells = [];
    for (let i = 0; i < height; i++) {
      cells.push([]);
      for (let j = 0; j < width; j++) {
        if (visibility[i] === undefined) {
          cells[i].push("nv");
        } else {
          const visibility_i = visibility[i];
          if (visibility_i[j] === undefined) {
            cells[i].push("nv");
          } else {
            cells[i].push(visibility[i][j]);
          }
        }
      }
    }
    console.log("Updating board", cells);
    setBoard(cells);
  }

  useEffect(
    (_) => {
      if (visibleState != null) {
        getVisibility();
      }
    },
    [visibleState]
  );

  return (
    <div className={`u-grid-${width}`}>
      {board.map((row, i) =>
        row.map((col, j) => (
          <UnderCell
            visibleState={visibleState}
            key={(i + 1) * (j + 1)}
            typeString={col}
            images={images}
          />
        ))
      )}
    </div>
  );
}
