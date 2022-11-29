import React, { useEffect, useState, useLayoutEffect } from "react";
import { useNavigate, useParams } from "react-router-dom";
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
import NavyLogo from "../components/NavyLogo";
import Chat from "../components/Chat";
import NavyTitle from "../components/NavyTitle";
import io from "socket.io-client";
import { API_URL as url } from "../API_URL";

const socket = io(`${url}`);
const NavyBoard = () => {
  const [game, setGame] = useState(null);
  const [accessDenied, setAccessDenied] = useState(true);
  const navigate = useNavigate();
  const { id } = useParams();
  const [missileSelected, setMissileSelected] = useState(false);
  const [missile, setMissile] = useState(null);
  const [myShip, setMyShip] = useState({});
  const [enemyShip, setEnemyShip] = useState(null);
  const [missiles, setMissiles] = useState(null);
  const [action, setAction] = useState({
    course: " ",
    move: 0,
    attack: 0,
  });
  const [move, setMove] = useState(false);
  const [actionSuccess, setActionSuccess] = useState(false);
  const [actionError, setActionError] = useState(false);
  const [winner, setWinner] = useState(null);
  const [openModal, setOpenModal] = useState(false);

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

  const handleNewCourse = (newCourse) => {
    setAction({ ...action, course: newCourse });
  };

  const handleAttack = () => {
    setAction({ ...action, attack: 1, move: 0 });
    setMove(false);
  };

  const handleMove = (quant) => {
    setMove(true);
    setAction({ ...action, attack: 0, move: quant });
  };

  const sendAction = () => {
    ActionService.sendAction(action)
      .then((resp) => {
        setActionSuccess(true);
        const timeout = setTimeout(() => {
          setActionSuccess(false);
          clearTimeout(timeout);
        }, 500);
        setMove(false);
        setAction({
          navy_game_id: resp.data.data.navy_game_id,
          ship_id: resp.data.data.ship_id,
          missile_type_id: resp.data.data.missile_type_id[0],
          round: resp.data.data.round + 1,
          course: resp.data.data.course,
          move: 0,
          attack: 0,
        });
      })
      .catch((err) => {
        const possibleErrorModal = err.response?.data?.message?.navy_game_id;
        if (possibleErrorModal) {
          if (possibleErrorModal.length > 0) {
            if (possibleErrorModal[0].includes("finished")) {
              setOpenModal(true);
            }
          }
        }
        setAction({
          course: " ",
          move: 0,
          attack: 0,
        });

        setActionError(true);
        const timeout = setTimeout(() => {
          setActionError(false);
          clearTimeout(timeout);
        }, 2000);
      });
  };

  const getShip = async (missile_type, ship) => {
    const data = await MissileService.getMissileTypes();
    const missiles = data.data.data;
    const missile = missiles[missile_type];
    const myShip = {
      ...ship,
      "missile speed": missile.speed,
      damage: missile.damage,
    };
    setMyShip(myShip);
  };

  const getEnemyShip = async (missile_type, ship) => {
    const data = await MissileService.getMissileTypes();
    const missiles = data.data.data;
    const missile = missiles[missile_type];
    const enemyShip = {
      ...ship,
      "missile speed": missile.speed,
      damage: missile.damage,
    };
    setEnemyShip(enemyShip);
  };

  const getGame = async () => {
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
          } else if (resp.data.data.status === "WAITING_PLAYERS") {
            navigate(`/navy/games/${id}/lobby`);
          }
        }

        if (resp.data.data.winner) {
          setOpenModal(true);
        }
        setWinner(resp.data.data.winner);
        setGame(resp.data.data);
        setMissiles(resp.data.data.sight_range.missiles);

        ShipService.getShipTypes().then((res) => {
          const shipType = res.data.data[resp.data.data.ship.name];
          const missile_type_id = shipType.missile_type_id[0];
          setAction({
            navy_game_id: resp.data.data.id,
            ship_id: resp.data.data.ship.id,
            missile_type_id: shipType.missile_type_id[0],
            round: resp.data.data.round,
            course: resp.data.data.ship.course,
            move: 0,
            attack: 0,
          });

          const ship = {
            name: resp.data.data.ship.name,
            hp: resp.data.data.ship.hp,
            course: resp.data.data.ship.course,
            x: resp.data.data.ship.pos_x,
            y: resp.data.data.ship.pos_y,
            size: resp.data.data.ship.size,
            speed: resp.data.data.ship.speed,
            "missile speed": 0,
            damage: 0,
          };
          getShip(missile_type_id, ship);

          if (resp.data.data.status !== "FINISHED") {
            if (resp.data.data.sight_range.ships.length !== 0) {
              const shipType =
                res.data.data[resp.data.data.sight_range.ships[0].name];
              const missile_type_id = shipType.missile_type_id[0];
              const enemyShip = {
                name: resp.data.data.sight_range.ships[0].name,
                hp: resp.data.data.sight_range.ships[0].hp,
                course: resp.data.data.sight_range.ships[0].course,
                x: resp.data.data.sight_range.ships[0].pos_x,
                y: resp.data.data.sight_range.ships[0].pos_y,
                size: resp.data.data.sight_range.ships[0].size,
                speed: resp.data.data.sight_range.ships[0].speed,
                "missile speed": 0,
                damage: 0,
              };
              getEnemyShip(missile_type_id, enemyShip);
            }
          }
        });

        setMyShip({
          name: resp.data.data.ship.name,
          hp: resp.data.data.ship.hp,
          course: resp.data.data.ship.course,
          x: resp.data.data.ship.pos_x,
          y: resp.data.data.ship.pos_y,
          size: resp.data.data.ship.size,
          speed: resp.data.data.ship.speed,
          "missile speed": 0,
          damage: 0,
        });

        setEnemyShip(null);

        if (resp.data.data.status !== "FINISHED") {
          if (resp.data.data.sight_range.ships.length !== 0) {
            setEnemyShip({
              name: resp.data.data.sight_range.ships[0].name,
              hp: resp.data.data.sight_range.ships[0].hp,
              course: resp.data.data.sight_range.ships[0].course,
              x: resp.data.data.sight_range.ships[0].pos_x,
              y: resp.data.data.sight_range.ships[0].pos_y,
              size: resp.data.data.sight_range.ships[0].size,
              speed: resp.data.data.sight_range.ships[0].speed,
              "missile speed": 0,
              damage: 0,
            });
          }
        }
      })
      .catch((resp) => {
        setGame({});
        setAccessDenied(true);
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
            <div>
              <h4 className="navy-text text-center mt-3 mb-0">
                The game ended
              </h4>
              <hr className="m-0" />
            </div>
            <h4 className="navy-text text-center m-0">
              {winner === authService.getCurrentUser().sub
                ? "you win!"
                : "you lose!"}
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
            <NavyLogo size={"small"} />
          </div>

          <div className="text-center">
            <div
              style={{ gap: "2rem" }}
              className="d-flex justify-content-center"
            >
              {game.round ? <NavyTitle text={"Round: " + game.round} /> : null}
              {game.turn ? (
                <NavyTitle
                  text={
                    "Turn: " +
                    (game.turn === game.user_1.id
                      ? game.user_1.username
                      : game.user_2.username)
                  }
                />
              ) : null}
            </div>
          </div>

          <div className="row mt-3">
            <div className="col-3">
              <div className="row justify-content-center">
                <div className="col-8">
                  <EntityDetails title={"My Ship"} data={myShip} />
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
                  />
                </div>
              </div>
              <div className="row justify-content-center mt-5">
                <div className="col-10">
                  <ActionCard
                    ship={myShip}
                    changeCourse={handleNewCourse}
                    changeAttack={handleAttack}
                    changeMove={handleMove}
                    attack={action.attack === 0 ? false : true}
                    move={move}
                  />
                </div>
              </div>
              {actionSuccess ? (
                <div className="row justify-content-center">
                  <Alert text={"Action sent successfully"} type={"success"} />
                </div>
              ) : null}
              {actionError ? (
                <div className="row justify-content-center">
                  <Alert text={"Error sending the action"} type={"danger"} />
                </div>
              ) : null}
              <div className="row justify-content-center">
                <div
                  style={{ gap: "1rem" }}
                  className="col-10 d-flex justify-content-center my-1"
                >
                  <NavyButton
                    text={"Send action"}
                    action={sendAction}
                    size={"small"}
                  />
                  <NavyButton
                    text={"Refresh"}
                    action={getGame}
                    size={"small"}
                  />
                </div>
              </div>
            </div>
            <div className="col-3">
              {enemyShip ? (
                <div className="row justify-content-center">
                  <div className="col-8 mb-2">
                    <EntityDetails title={"Enemy Ship"} data={enemyShip} />
                  </div>
                </div>
              ) : null}
              {missileSelected ? (
                <div className="row justify-content-center">
                  <div className="col-8">
                    <EntityDetails title={"Missile"} data={missile} />
                  </div>
                </div>
              ) : null}
            </div>
          </div>
        </>
      )}
    </div>
  );
};

export default NavyBoard;
