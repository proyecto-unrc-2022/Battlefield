import { useState, useEffect } from "react";
import "./css/game-style.css";

export default function UnderStats({ visibleState, currentUserId }) {
  const [currentUser, setCurrentUser] = useState(null);
  const [enemyUser, setEnemyUser] = useState(null);
  const [turn, setTurn] = useState(0);

  useEffect(
    (_) => {
      if (visibleState.host_id === currentUserId) {
        // If I am host
        setCurrentUser(visibleState.host);
        if (visibleState.visitor !== undefined)
          setEnemyUser(visibleState.visitor);
      } else {
        // If I am visitor
        if (visibleState.visitor !== undefined) {
          setCurrentUser(visibleState.visitor);
        }
        setEnemyUser(visibleState.host);
      }
      visibleState.turn === 0
        ? setTurn(visibleState.host.id)
        : setTurn(visibleState.visitor.id);
    },
    [visibleState, currentUserId]
  );

  function MyStats() {
    return (
      <div className="u-stats">
        <span>
          {currentUser === null
            ? null
            : currentUser.username + (turn === currentUserId ? " *" : "")}
        </span>
        <div className="u-stats-container">
          <div className="u-health-indicator">
            <img
              className="stat-img"
              alt="H"
              src={require("./css/icons/heart.png")}
            />
            <span>{visibleState.submarine.health}</span>
          </div>
          <div className="u-stat-indicator">
            <img
              alt="S"
              className="stat-img"
              src={require("./css/icons/speed.png")}
            />
            <span>{visibleState.submarine.speed}</span>
          </div>
          <div className="u-stat-indicator">
            <img
              alt="D"
              className="stat-img"
              src={require("./css/icons/torpedo-damage.png")}
            />
            <span>{visibleState.submarine.torpedo_damage}</span>
          </div>
          <div className="u-stat-indicator">
            <img
              alt="TS"
              className="stat-img"
              src={require("./css/icons/torpedo-speed.png")}
            />
            <span>{visibleState.submarine.torpedo_speed}</span>
          </div>
          <div className="u-stat-indicator">
            <img
              alt="RS"
              className="stat-img"
              src={require("./css/icons/radar-scope.png")}
            />
            <span>{visibleState.submarine.radar_scope}</span>
          </div>
        </div>
      </div>
    );
  }

  function EnemyStats() {
    return (
      <div className="u-stats u-enemy-stats">
        <span>
          {enemyUser === null
            ? null
            : (turn !== currentUserId ? "* " : "") + enemyUser.username}
        </span>
        <div className="u-stats-container">
          <div className="u-stat-indicator">
            <span>{visibleState.enemy_submarine.radar_scope}</span>
            <img
              alt="RS"
              className="stat-img"
              src={require("./css/icons/radar-scope.png")}
            />
          </div>
          <div className="u-stat-indicator">
            <span>{visibleState.enemy_submarine.torpedo_speed}</span>
            <img
              alt="TS"
              className="stat-img"
              src={require("./css/icons/torpedo-speed.png")}
            />
          </div>
          <div className="u-stat-indicator">
            <span>{visibleState.enemy_submarine.torpedo_damage}</span>
            <img
              alt="D"
              className="stat-img"
              src={require("./css/icons/torpedo-damage.png")}
            />
          </div>
          <div className="u-stat-indicator">
            <span>{visibleState.enemy_submarine.speed}</span>
            <img
              alt="S"
              className="stat-img"
              src={require("./css/icons/speed.png")}
            />
          </div>
          <div className="u-health-indicator">
            <span>{visibleState.enemy_submarine.health}</span>
            <img
              alt="H"
              className="stat-img"
              src={require("./css/icons/heart.png")}
            />
          </div>
        </div>
      </div>
    );
  }

  const style = {
    width: "100%",
    display: "flex",
    justifyContent: "space-between",
    alignItems: "center",
    margin: "25px 0",
  };

  return (
    <div style={style}>
      {visibleState.submarine !== undefined ? <MyStats /> : null}
      {visibleState.enemy_submarine !== undefined ? <EnemyStats /> : null}
    </div>
  );
}
