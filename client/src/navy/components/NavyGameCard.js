import React, { useEffect, useState } from "react";
import wings from "./../assets/wings.svg";
import NavyButton from "./NavyButton";
import NavyUserCard from "./NavyUserCard";
import "./NavyGameCard.css";
import authService from "../../services/auth.service";
import NavyGameService from "../services/NavyGameService";
import { useNavigate } from "react-router-dom";

const NavyGameCard = ({ game, button = "join" }) => {
  const [user2, setUser2] = useState({});
  const navigate = useNavigate();
  const currentUser = authService.getCurrentUser();

  const canJoin = () => {
    return (
      !(currentUser.sub !== game.user_1.id && currentUser.sub !== user2.id) ||
      freeToJoin()
    );
  };

  const freeToJoin = () => {
    return game.status === "WAITING_PLAYERS";
  };

  const joinPlayer = () => {
    if (freeToJoin()) {
      if (currentUser.sub === game.user_1.id) {
        navigate(`/navy/games/${game.id}/lobby`);
      } else {
        NavyGameService.patchNavyGame(game.id).then((res) => {
          navigate(`/navy/games/${game.id}/lobby`);
        });
      }
    } else if (game.status === "STARTED") {
      navigate(`/navy/games/${game.id}/board`);
    } else {
      navigate(`/navy/games/${game.id}/ship_selection`);
    }
  };

  const cancelGame = () => {
    NavyGameService.deleteNavyGame(game.id).then((res) => {
      navigate(`/navy`);
    });
  };

  const canSpectate = () => {
    return (game.status === "STARTED" || game.status === "FINISHED") && !canJoin();
  };

  const spectateGame = () => {
    navigate(`/navy/games/${game.id}/spectate_board`);
  };

  useEffect(
    () => {
      if (game.user_2) {
        setUser2(game.user_2);
      }
    },
    // eslint-disable-next-line
    []
  );

  return (
    <div className="navy-card-container d-flex flex-column align-items-center border border-dark pt-2 pb-2">
      <p className="navy-text m-0">{game.status.replace("_", " ")}</p>
      <div className="w-100 d-flex justify-content-center mb-2">
        <img src={wings} alt="Wings" />
      </div>
      <div className="w-75 d-flex justify-content-around align-items-center">
        <NavyUserCard username={game.user_1.username} />
        <p className="navy-text">VS.</p>
        <NavyUserCard
          username={Object.keys(user2).length !== 0 ? user2.username : ""}
          rol={Object.keys(user2).length !== 0 ? "guest" : "free"}
        />
      </div>
      {button === "join" && canJoin() ? (
        <div className="text-center">
          <NavyButton action={joinPlayer} text={"join"} size={"small"} />
        </div>
      ) : null}
      {button === "cancel-game" ? (
        <div className="text-center mt-2">
          <NavyButton action={cancelGame} text={"Cancel Game"} size={"small"} />
        </div>
      ) : null}
      {canSpectate() ? (
        <div className="text-center mt-2">
          <NavyButton action={spectateGame} text={"Spectate"} size={"small"} />
        </div>
      ) : null}

      <div className="d-flex justify-content-end w-75">
        <p className="navy-text m-0 p-0">GAME CODE: {game.id}</p>
      </div>
    </div>
  );
};

export default NavyGameCard;
