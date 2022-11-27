import React, { useState, useEffect } from "react";
import { useNavigate, useLocation, useParams } from "react-router-dom";
import NavyButton from "../components/NavyButton";
import ShipService from "../services/ShipService";
import NavyGameService from "../services/NavyGameService";
import authService from "../../services/auth.service";
import AccessDenied from "../components/AccessDenied";
import GridShipPlace from "../components/GridShipPlace";
import NavyTitle from "../components/NavyTitle";
import NavyLogo from "../components/NavyLogo";

export const NavyShipPlace = () => {
  const location = useLocation();
  const [ship, setShip] = useState(location.state?.ship_selected);
  const [shipPlaced, setShipPlaced] = useState(false);
  const navigate = useNavigate();
  const { id } = useParams();
  const [accessDenied, setAccessDenied] = useState(true);
  const [game, setGame] = useState(null);
  const [course, setCourse] = useState("N");
  const [selectedPosition, setSelectedPosition] = useState({});

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
      if (resp.data.data.ship) {
        setShipPlaced(true);
      }
      setGame(resp.data.data);

      let x = 5;
      let y = 5;
      if (currentUser.sub === resp.data.data.user_2.id) {
        y += 10;
      }
      setSelectedPosition({ x: x, y: y });
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

  const handleChangeCourse = (e) => {
    setCourse(e.target.value);
  };

  const selectPosition = (x, y) => {
    const currentUser = authService.getCurrentUser();
    if (currentUser.sub === game.user_2.id) {
      y += 10;
    }
    setSelectedPosition({
      x: x,
      y: y,
    });
  };

  const placeShip = () => {
    setShipPlaced(true);
    const shipToSend = {
      navy_game_id: ship.navy_game_id,
      name: ship.name,
      course: course,
      pos_x: selectedPosition.x,
      pos_y: selectedPosition.y,
    };
    ShipService.postShip(shipToSend).then((resp) => {
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
          <div className="row justify-content-between p-2 align-items-center">
            <NavyLogo size={"small"}></NavyLogo>
          </div>
          <div className="row">
            <div className="col-12 text-center">
              <NavyTitle text="Ship Place" size={4} />
            </div>
          </div>
          <div
            style={{ gap: "50px" }}
            className="row justify-content-center align mt-3"
          >
            <div>
              <p className="navy-text">Ship: {ship?.name}</p>
            </div>
            <div className="d-flex">
              <p className="navy-text m-0 mr-1">Course:</p>
              <select
                onChange={handleChangeCourse}
                className="custom-select custom-select-sm"
              >
                <option value={"N"}>N</option>
                <option value={"S"}>S</option>
                <option value={"E"}>E</option>
                <option value={"W"}>W</option>
                <option value={"NE"}>NE</option>
                <option value={"NW"}>NW</option>
                <option value={"SE"}>SE</option>
                <option value={"SW"}>SW</option>
              </select>
            </div>
            <div>
              <p className="navy-text">{`X: ${selectedPosition.x}, Y: ${selectedPosition.y}`}</p>
            </div>
          </div>
          <div className="row mx-auto mt-3">
            <GridShipPlace
              course={course}
              cols={game.cols}
              rows={game.rows}
              size={ship.size}
              selectPosition={selectPosition}
            />
          </div>
          <div className="row justify-content-center mt-3">
            {shipPlaced ? (
              <div className="row d-flex flex-column justify-content-center align-items-center">
                <div
                  style={{ color: "black" }}
                  className="spinner-border m-1"
                  role="status"
                >
                  <span className="sr-only">Loading...</span>
                </div>
                <span className="text-center navy-text">
                  Waiting for the other player select his ship...
                </span>
              </div>
            ) : (
              <NavyButton action={placeShip} text="Start Game" size={"small"} />
            )}
          </div>
        </>
      )}
    </div>
  );
};
