import React, { useState, useEffect } from 'react'; 
import "./css/game-style.css"

export default function UnderStats ({stats, enemyStats}) {
    const [maxHealth, setMaxHealth] = useState(null);
    const [maxEnemyHealth, setMaxEnemyHealth] = useState(null);

    function MyStats(){
        return (
            <div style={{display: 'flex', alignItems: 'center', gap: '10px'}}>
                <div className="u-health-indicator"><img alt="H" src="./css/icons/hearth.png" />{stats.health}</div>
                <div className="u-stat-indicator">{/* La imágen */}{stats.speed}</div>
                <div className="u-stat-indicator">{/* La imágen */}{stats.torpedo_damage}</div>
                <div className="u-stat-indicator">{/* La imágen */}{stats.torpedo_speed}</div>
                <div className="u-stat-indicator">{/* La imágen */}{stats.radar_scope}</div>
            </div>
        )
    }

    function EnemyStats() {
        return (
            <div style={{display: 'flex', alignItems: 'center', gap: '10px'}}>
                <div className="u-stat-indicator">{/* La imágen */}{enemyStats.radar_scope}</div>
                <div className="u-stat-indicator">{/* La imágen */}{enemyStats.torpedo_speed}</div>
                <div className="u-stat-indicator">{/* La imágen */}{enemyStats.torpedo_damage}</div>
                <div className="u-stat-indicator">{/* La imágen */}{enemyStats.speed}</div>
                <div className="u-health-indicator"><img alt="H" src="./css/icons/heart.png" />{enemyStats.health}</div>
            </div>
        )
    }

    return (
        <div style={{width: '100%', display: 'flex', justifyContent: 'space-between', alignItems: 'center'}}>
            <MyStats />
            { enemyStats != undefined ? <EnemyStats /> : null }
        </div>
    )
}