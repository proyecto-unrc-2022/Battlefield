import React, { useEffect, useState } from "react";
import NavyTitle from "./NavyTitle";
import Destroyer from "../assets/Destroyer.png";
import Cruiser from "../assets/Cruiser.svg";
import Battleship from "../assets/Battleship.svg";
import Corvette from "../assets/Corvette.svg";

import MissileService from "../services/MissileService";
import "./NavyShip.css";

const NavyShipCard = ({ ship, name, selectShip, selected = false }) => {
  const [missiles, setMissiles] = useState({});

  useEffect(() => {
    MissileService.getMissileTypes().then((resp) => {
      const missiles = resp.data.data;
      ship.missile_type_id.forEach((id) => {
        if (missiles[id]) {
          setMissiles((prev) => ({ ...prev, [id]: missiles[id] }));
        }
      });
    });
  }, []);

  const effectMouseEnterHover = (e) => {
    e.target.style.cursor = "pointer";
  };

  const getShipImage = () => {
    switch (name) {
      case "Destroyer":
        return Destroyer;
      case "Cruiser":
        return Cruiser;
      case "Battleship":
        return Battleship;
      case "Corvette":
        return Corvette;
      default:
        return null;
    }
  };

  return (
    <div
      className={
        "navy-card-ship-container d-flex flex-column align-items-center border border-dark py-4 mt-5 mb-3 " +
        (selected ? "selected" : "")
      }
      onMouseEnter={effectMouseEnterHover}
      onClick={(e) => {
        selectShip(name, ship);
      }}
    >
      <div className="w-100 d-flex justify-content-center mb-2">
        <NavyTitle text={name} size={8} />
      </div>

      <div className="w-75  d-flex justify-content-around align-items-center py-5">
        <img src={getShipImage()} alt="Ship" />
      </div>

      <div className="w-75 d-flex">
        <div className="d-flex flex-column">
          <p className="navy-text" style={{ margin: "0px" }}>
            Hp: {ship.hp}
          </p>

          <p className="navy-text" style={{ margin: "0px" }}>
            Size: {ship.size}{" "}
          </p>
          <p className="navy-text" style={{ margin: "0px" }}>
            Speed: {ship.speed}
          </p>
          {Object.keys(missiles).map((key) => {
            return (
              <div key={key}>
                <p className="navy-text" style={{ margin: "0px" }}>
                  Missile Type: {key}
                </p>

                <p className="navy-text" style={{ margin: "0px" }}>
                  Damage: {missiles[key].damage}
                </p>
                <p className="navy-text" style={{ margin: "0px" }}>
                  Speed: {missiles[key].speed}
                </p>
              </div>
            );
          })}
        </div>
      </div>
    </div>
  );
};

export default NavyShipCard;
