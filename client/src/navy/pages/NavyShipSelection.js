import React from "react";
import NavyTitle from "../components/NavyTitle";
import {  useState, useEffect } from "react";
import ShipService from "../services/ShipService";
import { Link ,useParams} from "react-router-dom";
import NavyButton from "../components/NavyButton";
import NavyShipCard from "../components/NavyShipCard";
import { useNavigate } from "react-router-dom";

const NavyShipSelection = () => {
  const navigate = useNavigate();
  const {id} = useParams();
  const [ships, setShips] = useState({});
  const [shipSelected, setShipSelected] = useState({
    navy_game_id: id /* game.id */,
  });

  useEffect(() => {
    ShipService.getShipTypes().then((resp) => {
      setShips(resp.data.data);
      console.log(resp.data.data);
    });
  }, []);

  const selectShip = (name) => {
    console.log(name);
    const ship = { ...shipSelected, name: name }
    setShipSelected(ship);
    console.log(shipSelected);
  };

  const goToPlaceToBoard = () => {
    console.log(shipSelected);
    navigate("place_ship", { state: { ship_selected: shipSelected } });
  };

  return (
    <div style={{ flexGrow: "1" }} className="container-fluid bg-navy">
      <div className="row justify-content-between p-2 align-items-center">
        <Link
          to={"/navy"}
          className="navy-text"
          style={{ textDecoration: "none" }}
        >
          Navy Battleship
        </Link>
      </div>

      <div className="row">
        <div className="col-12 text-center">
          <NavyTitle text="Ship Selection" size={4} />
        </div>
      </div>
      <div style={{ gap: "125px" }} className="row justify-content-center mb-3">
        {Object.keys(ships).map((key) => (
          <NavyShipCard
            key={ships[key].ship_id}
            ship={ships[key]}
            name={key}
            selectShip={selectShip}
          />
        ))}
      </div>

      <div className="row">
        <div className="col-2 text-center mx-auto mt-2">
          <NavyButton
            action={goToPlaceToBoard}
            text="Start Game"
            size={"medium"}
          />
        </div>
      </div>
    </div>
  );
};

export default NavyShipSelection;
