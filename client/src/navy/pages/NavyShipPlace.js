import React, { useState, useEffect } from "react";
import { useNavigate, useLocation, useParams } from "react-router-dom";
import NavyButton from "../components/NavyButton";
import ShipService from "../services/ShipService";
import NavyGameService from "../services/NavyGameService";
import authService from "../../services/auth.service";
import AccessDenied from "../components/AccessDenied";

export const NavyShipPlace = () => {
  const location = useLocation();
  const [ship, setShip] = useState(location.state?.ship_selected);
  const [shipPlaced, setShipPlaced] = useState(false);
  const navigate = useNavigate();
  const { id } = useParams();
  const [accessDenied, setAccessDenied] = useState(true);

  useEffect(() => {
    if (!location.state) {
      navigate(`/navy/games/${id}/ship_selection`);
    }

    NavyGameService.getNavyGame(id).then((resp) => {
      const currentUser = authService.getCurrentUser();
      const accessDenied =
        currentUser.sub !== resp.data.data.user_1.id &&
        currentUser.sub !== resp.data.data.user_2.id;

      setAccessDenied(accessDenied);
      if (!accessDenied) {
        if (resp.data.data.status === "STARTED") {
          navigate(`/navy/games/${id}/board`);
        } else if (resp.data.data.status === "WAITING_PLAYERS") {
          navigate(`/navy/games/${id}/lobby`);
        }
      }
    });

    if (shipPlaced) {
      const interval = setInterval(() => {
        NavyGameService.getNavyGame(ship.navy_game_id).then((resp) => {
          if (resp.data.data.status === "STARTED") {
            navigate(`/navy/games/${resp.data.data.id}/board`);
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
    <div style={{ flexGrow: "1" }} className="container-fluid bg-navy">
      {accessDenied ? (
        <AccessDenied
          text={"You can't join to this game"}
          buttonText={"Go to games"}
          redirectTo={"/navy/games"}
        />
      ) : (
        <>
          <h1>Ship: {ship?.name}</h1>
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
                  Waiting for the other player select his ship...
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
      )}
    </div>
  );
};
