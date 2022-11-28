import React from "react";
import { useNavigate } from "react-router-dom";
import NavyButton from "../components/NavyButton";
import NavyMenuStars from "../components/NavyMenuStars";
import NavyLogo from "../components/NavyLogo";
import NavyGameService from "../services/NavyGameService";

const NavyMenu = () => {
  const navigate = useNavigate();

  const goToGames = () => {
    navigate("games");
  };

  const createGame = () => {
    NavyGameService.postNavyGame().then((resp) => {
      navigate(`games/${resp.data.data.id}/lobby`);
    });
  };

  const goToHowToPlay = () => {
    navigate("how_to_play");
  };

  return (
    <div style={{ flexGrow: "1" }} className="container-fluid bg-menu">
      <div className="row">
        <div className="col-12 text-center">
          <NavyLogo size={"xlarge"} />
        </div>
      </div>
      <div className="row">
        <div className="col-5 text-center mx-auto mt-3">
          <NavyButton action={createGame} text="Create game" size={"large"} />
          <NavyMenuStars />
          <NavyButton action={goToGames} text="games" size={"large"} />
          <NavyMenuStars />
          <NavyButton
            action={goToHowToPlay}
            text="how to play"
            size={"large"}
          />
        </div>
      </div>
    </div>
  );
};

export default NavyMenu;
