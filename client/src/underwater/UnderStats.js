import React, { useState, useEffect } from 'react'; 
import "./css/game-style.css"

export default function UnderStats ({stats, enemyStats}) {
  const [maxHealth, setMaxHealth] = useState(null);
  const [maxEnemyHealth, setMaxEnemyHealth] = useState(null);

  function MyStats(){
    return (
      <div className="u-stats">
        <div className="u-health-indicator">
          <img className="stat-img" alt="H" src={require("./css/icons/heart.png")} />
          <span>{stats.health}</span>
        </div>
        <div className="u-stat-indicator">
          <img alt="S" className="stat-img" src={require("./css/icons/speed.png")} />
          <span>{stats.speed}</span>
        </div>
        <div className="u-stat-indicator">
          <img alt="D" className="stat-img" src={require("./css/icons/torpedo-damage.png")} />
          <span>{stats.torpedo_damage}</span>
        </div>
        <div className="u-stat-indicator">
          <img alt="TS" className="stat-img" src={require("./css/icons/torpedo-speed.png")} />
          <span>{stats.torpedo_speed}</span>
        </div>
        <div className="u-stat-indicator">
          <img alt="RS" className="stat-img" src={require("./css/icons/radar-scope.png")} />
          <span>{stats.radar_scope}</span>
        </div>
      </div>
    )
  }

  function EnemyStats() {
    return (
      <div className="u-stats">
        <div className="u-stat-indicator">
          <span>{enemyStats.radar_scope}</span>
          <img alt="RS" className="stat-img" src={require("./css/icons/radar-scope.png")} />
        </div>
        <div className="u-stat-indicator">
          <span>{enemyStats.torpedo_speed}</span>
          <img alt="TS" className="stat-img" src={require("./css/icons/torpedo-speed.png")} />
        </div>
        <div className="u-stat-indicator">
          <span>{enemyStats.torpedo_damage}</span>
          <img alt="D" className="stat-img" src={require("./css/icons/torpedo-damage.png")} />
        </div>
        <div className="u-stat-indicator">
          <span>{enemyStats.speed}</span>
          <img alt="S" className="stat-img" src={require("./css/icons/speed.png")} />
        </div>
        <div className="u-health-indicator">
          <span>{enemyStats.health}</span>
          <img alt="H" className="stat-img" src={require("./css/icons/heart.png")} />
        </div>
      </div>
    )
  }

  const style = {
    width: '100%',
    display: 'flex',
    justifyContent: 'space-between',
    alignItems: 'center',
    margin: '25px 0'
  }

  return (
    <div style={style}>
      { stats != undefined ? <MyStats /> : null }
      { enemyStats != undefined ? <EnemyStats /> : null }
    </div>
  )
}
