import { useEffect, useState } from "react";
import { Link } from "react-router-dom";
import authService from "../../services/auth.service";
import userService from "../../services/user.service";
import FiltersComponent from "../components/FiltersComponent";
import NavyGameCard from "../components/NavyGameCard";
import NavyTitle from "../components/NavyTitle";
import NavyGameService from "../services/NavyGameService";

const NavyGames = () => {
  const [games, setGames] = useState([]);
  const [filteredGames, setFilteredGames] = useState([]);

  useEffect(() => {
    NavyGameService.getNavyGames().then((resp) => {
      setGames(resp.data.data);
      setFilteredGames(resp.data.data);
    });
  }, []);

  const filterMyGames = () => {
    const currentUser = authService.getCurrentUser();
    setFilteredGames(
      games.filter(
        (game) =>
          game.user1_id === currentUser.sub || game.user2_id === currentUser.sub
      )
    );
  };

  const filterWaitingGames = () => {
    setFilteredGames(games.filter((game) => !game.user2_id));
  };

  const filterPlayingGames = () => {
    setFilteredGames(games.filter((game) => game.user2_id));
  };

  const filters = {
    "my-games": filterMyGames,
    "waiting": filterWaitingGames,
    "playing": filterPlayingGames,
  };

  const filterGames = (key) => {
    console.log(key)
    if (key in filters) {
      filters[key]();
    } else {
      setFilteredGames(games);
    }
  };

  return (
    <div style={{ flexGrow: "1" }} className="container-fluid bg-navy">
      <div className="row justify-content-between p-2 align-items-center">
        <Link
          to={"/navy"}
          className="navy-text"
          style={{ textDecoration: "none" }}
        >
          Navy Battlefield
        </Link>
        <FiltersComponent filter={filterGames} />
      </div>
      <div className="row">
        <div className="col-12 text-center">
          <NavyTitle text={"Games"} size={4} />
        </div>
      </div>
      <div style={{ gap: "20px" }} className="row justify-content-center mb-3">
        {filteredGames.map((game) => {
          return <NavyGameCard game={game} key={game.id} />;
        })}
      </div>
    </div>
  );
};

export default NavyGames;
