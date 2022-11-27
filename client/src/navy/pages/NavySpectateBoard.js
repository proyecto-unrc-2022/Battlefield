import React, { useEffect, useState,useContext } from "react";
import { useNavigate, useParams, Link } from "react-router-dom";
import authService from "../../services/auth.service";
import AccessDenied from "../components/AccessDenied";
import ActionCard from "../components/ActionCard";
import Alert from "../components/Alert";
import EntityDetails from "../components/EntityDetails";
import GridGame from "../components/GridGame";
import Modal from "../components/Modal";
import NavyButton from "../components/NavyButton";
import ActionService from "../services/ActionService";
import MissileService from "../services/MissileService";
import NavyGameService from "../services/NavyGameService";
import ShipService from "../services/ShipService";
import { SocketContext, socket } from "../context/socketContext";
import Chat from "../components/Chat";
import NavySpectateGameService from "../services/NavySpectateGameService";
import NavyTitle from "../components/NavyTitle";

const NavySpectateBoard = () => {
  const [game, setGame] = useState(null);
  const [accessDenied, setAccessDenied] = useState(true);
  const navigate = useNavigate();
  const { id } = useParams();
  const [missileSelected, setMissileSelected] = useState(false);
  const [missile, setMissile] = useState(null);
  const [myShip, setMyShip] = useState(null);
  const [enemyShip, setEnemyShip] = useState(null);
  const [missiles, setMissiles] = useState(null);
  const [action, setAction] = useState({
    course: " ",
    move: 0,
    attack: 0,
  });
  const [round, setRound] = useState(0);
  const [winner, setWinner] = useState(null);
  const [errorNext, setErrorNext] = useState(false);
  const [errorPrev, setErrorPrev] = useState(false);
  const [openModal, setOpenModal] = useState(false);
  const [specRound, setSpecRound] = useState(0);


  useEffect(() => {
    getGame()
   
  }, []);

  const handleSelectMissile = (missile) => {
    setMissileSelected(true);
    setMissile({
      course: missile.course,
      x: missile.pos_x,
      y: missile.pos_y,
      speed: missile.speed,
      damage: missile.damage,
    });
  };


  

  const getGame = (roundToSpec=0) => {
    
     return NavySpectateGameService.getNavySpectateGames(id,roundToSpec)
      .then((resp) => {

        const currentUser = authService.getCurrentUser();

        setAccessDenied(false);
       
        if(round == 0){
        setRound(resp.data.data.game.round-1);
        setSpecRound(resp.data.data.game.round-1);
        }

        if (resp.data.data.winner) {
          setOpenModal(true);
        }
        setWinner(resp.data.data.game.winner);
        setGame(resp.data.data.game);
        setMissiles(resp.data.data.missiles);
       
        
        setMyShip({
          name: resp.data.data.ships[0].name,
          hp: resp.data.data.ships[0].hp,
          course: resp.data.data.ships[0].course,
          x: resp.data.data.ships[0].pos_x,
          y: resp.data.data.ships[0].pos_y,
          size: resp.data.data.ships[0].size,
          speed: resp.data.data.ships[0].speed,
        });

        setEnemyShip(null);

        if (resp.data.data.status !== "FINISHED") {
            setEnemyShip({
              name: resp.data.data.ships[1].name,
              hp: resp.data.data.ships[1].hp,
              course: resp.data.data.ships[1].course,
              x: resp.data.data.ships[1].pos_x,
              y: resp.data.data.ships[1].pos_y,
              size: resp.data.data.ships[1].size,
              speed: resp.data.data.ships[1].speed,
            });
        }
      })
      

  };

  const prevRound = () => {
    const roundPrev = round-1;
    setRound(roundPrev);
    setSpecRound(roundPrev);
    setErrorPrev(false);

    getGame(roundPrev).catch((err) => {
      setErrorPrev(true);
      const roundNext = roundPrev+1;
      setRound(roundNext);
      const delay = 500;
      setTimeout(() => {
      setSpecRound(roundNext);
        
        setErrorPrev(false);
      }, delay);
    });
    
  };

  const nextRound = () => {
    const roundNext = round+1;
    setRound(roundNext);
    setSpecRound(roundNext)
    setErrorNext(false);

    getGame(roundNext).catch((err) => {
      setErrorNext(true);
      const roundPrev = roundNext-1;
      setRound(roundPrev);
      const delay = 500;
      setTimeout(() => {
        setSpecRound(roundPrev)
        setErrorNext(false);
      }, delay);
    });

  
  }; 



  return (
    <div style={{ flexGrow: "1" }} className="container-fluid bg-navy">
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
          <Modal isOpen={openModal}>
            <div
              className="d-flex justify-content-end pr-2"
              role={"button"}
              onClick={() => setOpenModal(false)}
            >
            </div>
            <h2 className="navy-text text-center">
              {winner === authService.getCurrentUser().sub
                ? "you win!"
                : "you lose!"}
            </h2>
            <p className="navy-text text-center">The game is over.</p>
            <div className="text-center">
              <button className="navy-text bg-white" onClick={() => navigate("/navy/games")}>Go to Games</button>
            </div>
          </Modal>
          <div className="row justify-content-between p-2 align-items-center">
            <Link
              to={"/navy"}
              className="navy-text"
              style={{ textDecoration: "none" }}
            >
              Navy Battleship
            </Link>
          </div>
          <div className="text-center">
            <NavyTitle text={
              !(errorPrev || errorNext) ? (
              "Round: "+ specRound ) : ("Unnaccesible Round")}/>
            </div>
          <div className="row mt-3">
            <div className="col-3">
              <div className="row justify-content-center">
                <div className="col-8">
                  <EntityDetails title={"Host"} data={myShip} />
                </div>
              
              <div className="col-12 d-flex flex column mt-5" >
                  <Chat
                    user={authService.getCurrentUser().username}
                    game={game}
                  />
              </div>
              </div>
            </div>
            <div className="col-6">
              <div className="row justify-content-center">
                <div className="col-12 d-flex justify-content-center">
                  <GridGame
                    rows={game.rows}
                    cols={game.cols}
                    myShip={myShip}
                    enemyShip={enemyShip}
                    missiles={missiles}
                    selectMissile={handleSelectMissile}
                    spectate={true}
                  />
                </div>
              </div>
              <div className="row justify-content-center mt-5">
                <div className="col-10">
                
                </div>
              </div>
             
              <div className="row justify-content-center">
                <div
                  style={{ gap: "1rem" }}
                  className="col-10 d-flex justify-content-center my-1"
                >
                  <NavyButton
                    text={"Previous"}
                    action={prevRound}
                    size={"small"}
                  />
                  <NavyButton
                    text={"Next"}
                    action={nextRound}
                    size={"small"}
                  />
                </div>

              </div>
              
              <div className="row justify-content-center">
                  {errorPrev || errorNext ? (
                    
                  <Alert text={"Unaccesible round"} type={"danger"} 
                  />) : null}
                </div>
            </div>
            {enemyShip ? (
              <div className="col-3">
                <div className="row justify-content-center">
                  <div className="col-8">
                    <EntityDetails title={"Guest"} data={enemyShip} />
                  </div>
                </div>
                {missileSelected ? (
                  <div className="row justify-content-center">
                    <div className="col-8 mt-2">
                      <EntityDetails title={"Missile"} data={missile} />
                    </div>
                  </div>
                ) : null}
              </div>
            ) : null}
          </div>
        </>
      )}
    </div>
  );
};

export default NavySpectateBoard;
