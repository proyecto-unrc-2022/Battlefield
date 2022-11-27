import { useNavigate } from "react-router-dom";
import NavyGameService from "../../services/NavyGameService";
import NavyButton from "../NavyButton";
import NavyTitle from "../NavyTitle";

const NavySlide6 = () => {

  const navigate = useNavigate()

  const createGame = () => {
    NavyGameService.postNavyGame().then((resp) => {
      navigate(`/navy/games/${resp.data.data.id}/lobby`);
    });
  };

  return (
    <div className="text-break">
      <NavyTitle text="Some important things to keep in mind." size="medium" />
      <p className="text-justify">
        Inside the game board you can have parts of a ship outside of it, except
        for the bow. Also, the maximum travel distance and forward speed of
        missiles are entirely dependent on the type of ship that is selected at
        the start of the game.
      </p>
      <NavyTitle text="¡Enjoy Navy Battleship!" size="medium" />
      <div style={{gap: "5px"}} className="d-flex justify-content-center">
        <NavyButton size={"small"} text={"Create game"} action={createGame}/>
        <NavyButton size={"small"} text={"Explore games"} action={() => navigate("/navy/games")}/>
      </div>
    </div>
  );
};

export default NavySlide6;
