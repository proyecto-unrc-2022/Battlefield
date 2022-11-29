import React, { useEffect, useState } from "react";
import { useNavigate, useParams } from "react-router-dom";
import NavyGameService from "../services/NavyGameService";
import NavyGameCard from "../components/NavyGameCard";
import NavyTitle from "../components/NavyTitle";
import NavyLogo from "../components/NavyLogo";
import authService from "../../services/auth.service";
import AccessDenied from "../components/AccessDenied";

const NavyLobby = () => {
  const { id } = useParams();
  const [game, setGame] = useState(null);
  const [accessDenied, setAccessDenied] = useState(true);
  const navigate = useNavigate();

  useEffect(() => {
    let interval;

    NavyGameService.getNavyGame(id)
      .then((resp) => {
        const currentUser = authService.getCurrentUser();
        const accessDenied =
          currentUser.sub !== resp.data.data.user_1.id &&
          currentUser.sub !== resp.data.data.user_2.id;

        setAccessDenied(accessDenied);

        if (!accessDenied) {
          if (resp.data.data.status === "WAITING_PICKS") {
            navigate(`/navy/games/${id}/ship_selection`);
          } else if (resp.data.data.status === "STARTED") {
            navigate(`/navy/games/${id}/board`);
          } else {
            interval = setInterval(() => {
              NavyGameService.getNavyGame(id).then((resp) => {
                if (resp.data.data.status === "WAITING_PICKS") {
                  navigate(`/navy/games/${id}/ship_selection`);
                }
              });
            }, 5000);
          }
        }
        setGame(resp.data.data);
      })
      .catch((resp) => {
        setGame({});
        setAccessDenied(true);
      });
    return () => clearInterval(interval);
  }, []);

  return (
    <div style={{ flexGrow: "1" }} className="container-fluid bg-menu">
      <div className="row justify-content-between p-2 align-items-center">
        <NavyLogo size={"small"} />
      </div>
      {!game ? (
        <div className="row mt-5">
          <div className="col-12 text-center">
            <div className="spinner-border" role="status">
              <span className="sr-only">Loading...</span>
            </div>
          </div>
        </div>
      ) : accessDenied ? (
        <AccessDenied
          text={"You can't join to this game"}
          buttonText={"Go to games"}
          redirectTo={"/navy/games"}
        />
      ) : (
        <>
          <div className="row">
            <div className="col-12 text-center">
              <NavyTitle text="Navy Battleship" size={2} />
            </div>
          </div>
          <div className="row">
            <div className="col-12 d-flex justify-content-center mt-4">
              {game ? (
                <NavyGameCard
                  button={"cancel-game"}
                  game={game}
                  key={game.id}
                />
              ) : null}
            </div>
          </div>
          <div className="row d-flex flex-column align-items-center mt-3">
            <div className="spinner-border" role="status">
              <span className="sr-only">Loading...</span>
            </div>
            <div className="d-flex justify-content-center mt-2">
              <NavyTitle text="Waiting for another player" size={5} />
            </div>
          </div>
        </>
      )}
    </div>
  );
};
export default NavyLobby;
