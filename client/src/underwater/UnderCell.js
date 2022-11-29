import React from "react";
import "./css/game-style.css";
import { GoPrimitiveDot } from "react-icons/go";

export default function UnderCell({
  visibleState,
  placeSubmarine = null,
  x,
  y,
  typeString,
  images,
}) {
  let type = {};
  if (typeString !== undefined && typeString.length === 3) {
    type = {
      team: typeString[0],
      object: typeString[1],
      direction: parseInt(typeString[2]),
    };
    if (type.object === "H" || type.object === "T")
      type.subName =
        type.team === "F"
          ? visibleState.submarine.name
          : visibleState.enemy_submarine.name;
    else if (type.object === "*") type.subName = "Torpedo";
  }

  const rotation = type.direction === undefined ? 0 : 45 * type.direction;

  const style = {
    transform: `rotate(${rotation}deg)`,
  };

  function image() {
    if (type.object === "H" || type.object === "T" || type.object === "*")
      return type.subName === undefined ? null : (
        <img
          alt="cell"
          style={style}
          src={images[type.subName][type.team][type.object]}
          width="100%"
        />
      );
    if (typeString === "rP")
      return <GoPrimitiveDot style={{ color: "cyan" }} />;
    return null;
  }

  return (
    <div
      onClick={placeSubmarine === null ? null : (_) => placeSubmarine(x, y)}
      className={`u-cell u-cell-${typeString}`}
    >
      {image()}
    </div>
  );
}
