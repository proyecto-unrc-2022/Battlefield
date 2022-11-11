import React, { useState, useEffect } from "react";
import { useNavigate, useLocation } from "react-router-dom";
import NavyButton from "../components/NavyButton";
import ShipService from "../services/ShipService";
import NavyGameService from "../services/NavyGameService";

export const NavyShipPlace = () => {
  const location = useLocation();
  const [ship, setShip] = useState(location.state.ship_selected);
  const [shipPlaced, setShipPlaced] = useState(false);
  const navigates = useNavigate();

  useEffect(() => {
    if (shipPlaced) {
      const interval = setInterval(() => {
        NavyGameService.getNavyGame(ship.navy_game_id).then((resp) => {
          console.log(resp.data);
          if (resp.data.data.ready_to_play) {
            navigates("/navy");
          }
        });
      }, 5000);
      return () => clearInterval(interval);
    }
  }, [shipPlaced]);

  const handleXCord = (e) => {
    setShip((prev) => ({ ...prev, pos_x: e.target.value }));
  };

  const handleYCord = (e) => {
    setShip((prev) => ({ ...prev, pos_y: e.target.value }));
  };

  const handleCourse = (e) => {
    setShip((prev) => ({ ...prev, course: e.target.value }));
  };

  const placeShip = () => {
    setShipPlaced(true);
    ShipService.postShip(ship).then((resp) => {
      console.log(resp);
    });
  };

  return (
    <>
      <h1>Ship: {ship.name}</h1>
      <div className="row justify-content-center">
        <div className="col-3 col-md-3 mx-auto">
          <form>
            <div className="form-group">
              <label htmlFor="x">X</label>
              <input
                onChange={handleXCord}
                type="number"
                className="form-control"
                id="x"
                placeholder="X"
              />
            </div>
            <div className="form-group">
              <label htmlFor="y">Y</label>
              <input
                onChange={handleYCord}
                type="number"
                className="form-control"
                id="y"
                placeholder="Y"
              />
            </div>

            <div className="form-group">
              <label htmlFor="y">COURSE</label>
              <input
                onChange={handleCourse}
                type="text"
                className="form-control"
                id="y"
                placeholder="N"
              />
            </div>
          </form>
        </div>
      </div>
      <div className="row justify-content-center">
        {shipPlaced ? (
          <div className="row d-flex flex-column justify-content-center align-items-center">
            <div className="spinner-border m-3" role="status">
              <span className="sr-only">Loading...</span>
            </div>
            <span className="text-center">
              Waiting for the other player select him ship...
            </span>
          </div>
        ) : (
          <NavyButton
            action={placeShip}
            text="Place and Play"
            size={"medium"}
          />
        )}
      </div>
    </>
  );
};
