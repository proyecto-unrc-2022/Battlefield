import SlideShipCard from "./SlideShipCard";
import { useState, useEffect } from "react";
import ShipService from "../../services/ShipService";

const NavySlide2 = () => {
  const [ships, setShips] = useState({});
  const [shipSelected, setShipSelected] = useState({ });
  
  const selectShip = (name, ship) => {
    const navy_ship = { ...shipSelected, name: name, size: ship.size };
    setShipSelected(navy_ship);
  };

  useEffect(() => {
    ShipService.getShipTypes().then((resp) => {
      setShips(resp.data.data);
    });
  }, []);

  return (
    <div className="text-break">
      <p className="text-justify">
        When you enter a game, you must choose one of the existing ships. Once
        the ship has been chosen, you must wait until the other player has made
        his selection.
      </p>
      <div style={{ gap: "40px" }} className="row justify-content-center mb-2">
        {Object.keys(ships).map((key) => (
          <SlideShipCard
            key={ships[key].ship_id}
            ship={ships[key]}
            name={key}
            selectShip={selectShip}
            selected={shipSelected.name === key}
          />
        ))}
      </div>
    </div>
  );
};

export default NavySlide2;
