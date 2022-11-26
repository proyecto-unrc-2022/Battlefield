import React, { useState, useEffect } from 'react'; 
import "./css/game-style.css"

export default function UnderStats ({visibleState}) {

  function MyStats(){
    return (
      <div className="u-stats">
        <div className="u-health-indicator">
          <img className="stat-img" alt="H" src={require("./css/icons/heart.png")} />
          <span>{visibleState.submarine.health}</span>
        </div>
        <div className="u-stat-indicator">
          <img alt="S" className="stat-img" src={require("./css/icons/speed.png")} />
          <span>{visibleState.submarine.speed}</span>
        </div>
        <div className="u-stat-indicator">
          <img alt="D" className="stat-img" src={require("./css/icons/torpedo-damage.png")} />
          {visibleState.submarine.torpedo_damage}
        </div>
        <div className="u-stat-indicator">
          <img alt="TS" className="stat-img" src={require("./css/icons/torpedo-speed.png")} />
          {visibleState.submarine.torpedo_speed}
        </div>
        <div className="u-stat-indicator">
          <img alt="RS" className="stat-img" src={require("./css/icons/radar-scope.png")} />
          {visibleState.submarine.radar_scope}
        </div>
      </div>
    )
  }

  function EnemyStats() {
    return (
      <div className="u-stats">
        <div className="u-stat-indicator">
          {visibleState.enemy_submarine.radar_scope}
          <img alt="RS" className="stat-img" src={require("./css/icons/radar-scope.png")} />
        </div>
        <div className="u-stat-indicator">
          {visibleState.enemy_submarine.torpedo_speed}
          <img alt="TS" className="stat-img" src={require("./css/icons/torpedo-speed.png")} />
        </div>
        <div className="u-stat-indicator">
          {visibleState.enemy_submarine.torpedo_damage}
          <img alt="D" className="stat-img" src={require("./css/icons/torpedo-damage.png")} />
        </div>
        <div className="u-stat-indicator">
          <span>{visibleState.enemy_submarine.speed}</span>
          <img alt="S" className="stat-img" src={require("./css/icons/speed.png")} />
        </div>
        <div className="u-health-indicator">
          <span>{visibleState.enemy_submarine.health}</span>
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
      { visibleState.submarine != undefined ? <MyStats /> : null }
      { visibleState.enemy_submarine != undefined ? <EnemyStats /> : null }
    </div>
  )
}
