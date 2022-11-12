import React, { useEffect, useState } from "react";
import { useParams } from "react-router-dom";
import NavyGameService from "../services/NavyGameService";
import NavyGameCard from "../components/NavyGameCard";
import NavyTitle from "../components/NavyTitle";
import ReactLoading from "react-loading";

const NavyLobby = () => {
  const {id} = useParams();
  const [game, setGame] = useState(null);

  useEffect(() => {
    NavyGameService.getNavyGame(id).then((resp) => {
      setGame(resp.data.data);
    });
  }, []);

  return (
    <div style={{ flexGrow: "1" }} className="container-fluid bg-navy">
      <div className="row">
        <div className="col-12 text-center">
          <NavyTitle text="Navy Battleship" size={2} />
        </div>
      </div>
      <div className="row">
        <div className="col-12 row justify-content-center mt-4">
          {game ? <NavyGameCard game={game} key={game.id} /> : null}
        </div>
      </div>
      <div className="row d-flex flex-column">
        <div className="d-flex justify-content-center mt-2">
          <ReactLoading type="spin" color="#000" />
        </div>
        <div className="d-flex justify-content-center mt-2">
          <NavyTitle text="Waiting for another player" size={5} />
        </div>
      </div>
    </div>
  );
};
export default NavyLobby;
