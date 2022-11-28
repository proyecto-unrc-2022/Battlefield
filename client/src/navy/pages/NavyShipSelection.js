import React from "react";
import NavyTitle from "../components/NavyTitle";
import { useState, useEffect } from "react";
import ShipService from "../services/ShipService";
import { useParams } from "react-router-dom";
import NavyButton from "../components/NavyButton";
import NavyLogo from "../components/NavyLogo";
import NavyShipCard from "../components/NavyShipCard";
import { useNavigate } from "react-router-dom";
import NavyGameService from "../services/NavyGameService";
import authService from "../../services/auth.service";
import AccessDenied from "../components/AccessDenied";

const NavyShipSelection = () => {
  const navigate = useNavigate();
  const { id } = useParams();
  const [ships, setShips] = useState({});
  const [shipSelected, setShipSelected] = useState({
    navy_game_id: id,
  });
  const [accessDenied, setAccessDenied] = useState(true);

  useEffect(() => {
    ShipService.getShipTypes().then((resp) => {
      setShips(resp.data.data);
    });

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
        } else if (resp.data.data.status === "FINISHED") {
          navigate(`/navy/games/${id}/board`);
        }
      }
    });
  }, []);

  const selectShip = (name, ship) => {
    const navy_ship = { ...shipSelected, name: name, size: ship.size };
    setShipSelected(navy_ship);
  };

  const goToPlaceToBoard = () => {
    if ("name" in shipSelected) {
      navigate("place_ship", { state: { ship_selected: shipSelected } });
    }
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
            <div className="row justify-content-between p-2 align-items-center">
              <NavyLogo size={"small"} />
            </div>
          </div>
          <div className="row">
            <div className="col-12 text-center">
              <NavyTitle text="Ship Selection" size={4} />
            </div>
          </div>
          <div
            style={{ gap: "75px" }}
            className="row justify-content-center mb-3"
          >
            {Object.keys(ships).map((key) => (
              <NavyShipCard
                key={ships[key].ship_id}
                ship={ships[key]}
                name={key}
                selectShip={selectShip}
                selected={shipSelected.name === key}
              />
            ))}
          </div>

          <div className="row">
            <div className="col-2 text-center mx-auto my-2">
              <NavyButton
                action={goToPlaceToBoard}
                text="Place Ship"
                size={"small"}
              />
            </div>
          </div>
        </>
      )}
    </div>
  );
};

export default NavyShipSelection;
