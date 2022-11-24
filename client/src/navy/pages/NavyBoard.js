import React, { useEffect, useState } from "react";
import { useNavigate, useParams, Link } from "react-router-dom";
import authService from "../../services/auth.service";
import AccessDenied from "../components/AccessDenied";
import ActionCard from "../components/ActionCard";
import EntityDetails from "../components/EntityDetails";
import GridGame from "../components/GridGame";
import NavyButton from "../components/NavyButton";
import NavyGameService from "../services/NavyGameService";

const NavyBoard = () => {
  const [game, setGame] = useState(null);
  const [accessDenied, setAccessDenied] = useState(true);
  const navigate = useNavigate();
  const { id } = useParams();
  const [missileSelected, setMissileSelected] = useState(false);
  const [missile, setMissile] = useState(null);
  const [myShip, setMyShip] = useState(null);
  const [enemyShip, setEnemyShip] = useState(null);
  const [missiles, setMissiles] = useState(null);

  useEffect(() => {
    NavyGameService.getNavyGame(id)
      .then((resp) => {
        console.log(resp.data.data);
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
        setGame(resp.data.data);
        setMissiles(resp.data.data.sight_range.missiles);
        setMyShip({
          name: resp.data.data.ship.name,
          hp: resp.data.data.ship.hp,
          course: resp.data.data.ship.course,
          x: resp.data.data.ship.pos_x,
          y: resp.data.data.ship.pos_y,
          size: resp.data.data.ship.size,
          speed: resp.data.data.ship.speed,
        });
        if (resp.data.data.sight_range.ships.length !== 0) {
          setEnemyShip({
            name: resp.data.data.sight_range.ships[0].name,
            hp: resp.data.data.sight_range.ships[0].hp,
            course: resp.data.data.sight_range.ships[0].course,
            x: resp.data.data.sight_range.ships[0].pos_x,
            y: resp.data.data.sight_range.ships[0].pos_y,
            size: resp.data.data.sight_range.ships[0].size,
            speed: resp.data.data.sight_range.ships[0].speed,
          });
        }
      })
      .catch((resp) => {
        setGame({});
        setAccessDenied(true);
      });
  }, []);

  const handleSelectMissile = (missile) => {
    setMissileSelected(true)
    setMissile({
      course: missile.course,
      x: missile.pos_x,
      y: missile.pos_y,
      speed: missile.speed,
      damage: missile.damage
    })
  }

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
          <div className="row justify-content-between p-2 align-items-center">
            <Link
              to={"/navy"}
              className="navy-text"
              style={{ textDecoration: "none" }}
            >
              Navy Battleship
            </Link>
          </div>
          <div className="row mt-3">
            <div className="col-3">
              <div className="row justify-content-center">
                <div className="col-8">
                  <EntityDetails title={"My Ship"} data={myShip} />
                </div>
              </div>
            </div>
            <div className="col-6">
              <div className="row justify-content-center">
                <div className="col-12">
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
                  <ActionCard />
                </div>
              </div>
              <div className="row justify-content-center my-3">
                <div style={{gap: "1rem"}} className="col-10 d-flex justify-content-center">
                  <NavyButton text={"Send action"}/>
                  <NavyButton text={"Refresh"}/>
                </div>
              </div>
            </div>
            {enemyShip ? (
              <div className="col-3">
                <div className="row justify-content-center">
                  <div className="col-8">
                    <EntityDetails title={"My Ship"} data={enemyShip} />
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

export default NavyBoard;
