import React, { useEffect, useLayoutEffect, useState } from "react";
import { useNavigate, useParams } from "react-router-dom";
import NavyGameService from "../services/NavyGameService";
import NavyGameCard from "../components/NavyGameCard";
import NavyTitle from "../components/NavyTitle";
import ReactLoading from "react-loading";

const NavyLobby = () => {
  const { id } = useParams();
  const [game, setGame] = useState(null);
  const navigate = useNavigate();

  useLayoutEffect(() => {
    NavyGameService.getNavyGame(id).then((resp) => { 
      if ("id" in resp.data.data.user_2) {
        navigate(`/navy/games/${id}/ship_selection`);
      }
    });
    
  }, [])

  useEffect(() => {
    NavyGameService.getNavyGame(id).then((resp) => {
      setGame(resp.data.data);
    });

    const interval = setInterval(() => {
      NavyGameService.getNavyGame(id).then((resp) => {
        if ("id" in resp.data.data.user_2) {
          navigate(`/navy/games/${id}/ship_selection`);
        }
      });
      
    }, 5000);
    return () => clearInterval(interval);
  }, []);

  return (
    <div style={{ flexGrow: "1" }} className="container-fluid bg-navy">
      <div className="row">
        <div className="col-12 text-center">
          <NavyTitle text="Navy Battleship" size={2} />
        </div>
      </div>
      <div className="row">
        <div className="col-12 d-flex justify-content-center mt-4">
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
