import React from "react";
import NavyTitle from "../components/NavyTitle";
import { useState, useEffect } from "react";
import ShipService from "../services/ShipService";

const NavyShipSelection = () => {
  const [ships, setShips] = useState({});

  useEffect(() => {
    ShipService.getShipTypes().then((resp) => {
      setShips(resp.data.data);
      console.log(resp.data.data);
    });
  }, []);

  return (
    <div style={{ flexGrow: "1" }} className="container-fluid bg-navy">
      <div className="row"></div>

      <div className="row">
        <div className="col-12 text-center">
          <NavyTitle text="Ship Selection" size={4} />
        </div>
      </div>
      <div className="row"></div>
    </div>
  );
};

export default NavyShipSelection;
