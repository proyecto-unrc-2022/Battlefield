import React, { useEffect, useState } from "react";
import { useNavigate, useParams, Link } from "react-router-dom";
import authService from "../../services/auth.service";
import AccessDenied from "../components/AccessDenied";
import Alert from "../components/Alert";
import EntityDetails from "../components/EntityDetails";
import GridGame from "../components/GridGame";
import Modal from "../components/Modal";
import NavyButton from "../components/NavyButton";
import Chat from "../components/Chat";
import NavySpectateGameService from "../services/NavySpectateGameService";
import NavyTitle from "../components/NavyTitle";
import userService from "../../services/user.service";
import { API_URL as url } from "../API_URL";
import { io } from "socket.io-client";

const socket = io(`${url}`);
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
  const [round, setRound] = useState(0);
  const [winner, setWinner] = useState(null);
  const [errorNext, setErrorNext] = useState(false);
  const [errorPrev, setErrorPrev] = useState(false);
  const [openModal, setOpenModal] = useState(false);
  const [specRound, setSpecRound] = useState(0);

  useEffect(() => {
    if (!game) {

      getGame();
      if (socket.disconnect) {
        socket.connect();
      }
    }

    return () => {
      socket.close();
    };
  }, [socket]);

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

  const getGame = async (roundToSpec = 0) => {
    return NavySpectateGameService.getNavySpectateGames(id, roundToSpec).then(
      (resp) => {
        setAccessDenied(false);

        if (round === 0) {
          setRound(resp.data.data.game.round - 1);
          setSpecRound(resp.data.data.game.round - 1);
        }
        if (
          resp.data.data.game.status === "FINISHED" &&
          resp.data.data.game.round === roundToSpec
        ) {
          setOpenModal(true);
        }
        setWinner(resp.data.data.game.winner);
        setGame(resp.data.data.game);
        setMissiles(resp.data.data.missiles);
        console.log(resp.data.data.game.user_1.id)
        console.log(resp.data.data.ships[0].user_id)
        let user_temp = false
        if(resp.data.data.game.user_1.id === resp.data.data.ships[0].user_id){
          user_temp = true
        setMyShip({
          name: resp.data.data.ships[0].name,
          hp: resp.data.data.ships[0].hp,
          course: resp.data.data.ships[0].course,
          x: resp.data.data.ships[0].pos_x,
          y: resp.data.data.ships[0].pos_y,
          size: resp.data.data.ships[0].size,
          speed: resp.data.data.ships[0].speed,
        });
      }else{
        setMyShip({
          name: resp.data.data.ships[1].name,
          hp: resp.data.data.ships[1].hp,
          course: resp.data.data.ships[1].course,
          x: resp.data.data.ships[1].pos_x,
          y: resp.data.data.ships[1].pos_y,
          size: resp.data.data.ships[1].size,
          speed: resp.data.data.ships[1].speed,
        });
      }
        setEnemyShip(null);

        if (resp.data.data.status !== "FINISHED") {
          if(user_temp){
          setEnemyShip({
            name: resp.data.data.ships[1].name,
            hp: resp.data.data.ships[1].hp,
            course: resp.data.data.ships[1].course,
            x: resp.data.data.ships[1].pos_x,
            y: resp.data.data.ships[1].pos_y,
            size: resp.data.data.ships[1].size,
            speed: resp.data.data.ships[1].speed,
          });
        }else{
          setEnemyShip({
            name: resp.data.data.ships[0].name,
            hp: resp.data.data.ships[0].hp,
            course: resp.data.data.ships[0].course,
            x: resp.data.data.ships[0].pos_x,
            y: resp.data.data.ships[0].pos_y,
            size: resp.data.data.ships[0].size,
            speed: resp.data.data.ships[0].speed,
          });
        }
      }
      }
    );
  };

  const prevRound = () => {
    const roundPrev = round - 1;
    setRound(roundPrev);
    setSpecRound(roundPrev);
    setErrorPrev(false);

    getGame(roundPrev).catch((err) => {
      setErrorPrev(true);
      const roundNext = roundPrev + 1;
      setRound(roundNext);
      const delay = 500;

      setTimeout(() => {
        setSpecRound(roundNext);
        setErrorPrev(false);
      }, delay);
    });
  };

  const nextRound = () => {
    const roundNext = round + 1;
    setRound(roundNext);
    setSpecRound(roundNext);
    setErrorNext(false);

    getGame(roundNext).catch((err) => {
      setErrorNext(true);
      const roundPrev = roundNext - 1;
      setRound(roundPrev);
      const delay = 500;
      setTimeout(() => {
        setSpecRound(roundPrev);
        setErrorNext(false);
      }, delay);
    });
  };

  return (
    <div style={{ flexGrow: "1" }} className="container-fluid bg-navy">
      {false ? (
        <div className="row mt-5">
          <div className="col-12 text-center">
            <div className="spinner-border" role="status">
              <span className="sr-only">Loading...</span>
            </div>
          </div>
        </div>
      ) : accessDenied ? (
        <AccessDenied
          text={
            "The game you are trying to spectate its under 3 rounds, please check later"
          }
          buttonText={"Go to games"}
          redirectTo={"/navy/games"}
        />
      ) : (
        <>
          <Modal isOpen={openModal}>
            <div>
              <h4 className="navy-text text-center mt-3 mb-0">
                The game ended
              </h4>
              <hr className="m-0" />
            </div>
            <h4 className="navy-text text-center m-0">
              <span>
                {" "}
                {game.winner === game.user_1.id
                  ? `${game.user_1.username} WON!`
                  : `${game.user_2.username} WON!`}
              </span>
            </h4>
            <div className="text-center">
              <div>
                <hr className="m-0" />

                <div
                  style={{ gap: "5px" }}
                  className="d-flex justify-content-end pr-3 py-2"
                >
                  <NavyButton
                    text={"Close"}
                    action={() => setOpenModal(false)}
                    size={"small"}
                  />
                  <NavyButton
                    text={"Go to games"}
                    action={() => navigate("/navy/games")}
                    size={"small"}
                  />
                </div>
              </div>
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
            <NavyTitle
              text={
                !(errorPrev || errorNext)
                  ? "Round: " + specRound
                  : "Unnaccesible Round"
              }
            />
          </div>
          <div className="row mt-3">
            <div className="col-3">
              <div className="row justify-content-center">
                <div className="col-8">
                  <EntityDetails
                    title={`${game.user_1.username}`}
                    data={myShip}
                    game={game}
                  />
                </div>

                {socket ? (
                  <div className="col-12 d-flex flex column mt-3">
                    <Chat
                      user={authService.getCurrentUser().username}
                      game={game}
                      socket={socket}
                    />
                  </div>
                ) : null}
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
                <div className="col-10"></div>
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
                  <NavyButton text={"Next"} action={nextRound} size={"small"} />
                </div>
              </div>

              <div className="row justify-content-center">
                {errorPrev || errorNext ? (
                  <Alert text={"Unaccesible round"} type={"danger"} />
                ) : null}
              </div>
            </div>
            {enemyShip ? (
              <div className="col-3">
                <div className="row justify-content-center">
                  <div className="col-8">
                    <EntityDetails
                      title={`${game.user_2.username}`}
                      data={enemyShip}
                      game={game}
                    />
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
