import React, { useEffect, useState } from "react";
import NavyGameCard from "../components/NavyGameCard";
import NavyTitle from "../components/NavyTitle";
import NavyGameService from "../services/NavyGameService";

const NavyGames = () => {
  const [games, setGames] = useState([]);

  useEffect(() => {
    NavyGameService.getNavyGames().then((resp) => {
      setGames(resp.data.data);
    });
  }, []);

  return (
    <div style={{ flexGrow: "1" }} className="container-fluid bg-navy">
      <div className="row">
        <div className="col-12 text-center">
          <NavyTitle text={"Games"} size={4} />
        </div>
      </div>
      <div className="row">
        {games.map((game) => {
          return <NavyGameCard game={game} key={game.id}/>;
        })}
      </div>
    </div>
  );
};

export default NavyGames;
