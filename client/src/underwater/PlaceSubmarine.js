import React, { useState, useEffect } from 'react';
import './css/game-style.css';
import AuthService from '../services/auth.service';
import UnderCell from './UnderCell';

export default function PlaceSubmarine(props) {
  const currentUserId = AuthService.getCurrentUser().sub;
  const [cells, setCells] = useState([]);

  useEffect(() => {
    const cells = [];
    for (let i = 0; i < props.height; i++) {
      cells.push([]);
      for (let j = 0; j < props.width; j++) {
        cells[i].push(`${i + 1},${j + 1}`);
      }
    }
    setCells(cells);
  }, []);

  function placeSubmarine(x, y) {
    const dir = y < props.width / 2 ? 2 : 6;
    props.setPosition({ x, y, direction: dir });
  }

  return (
    <div style={{ height: `${976 / 2}px` }} className={`u-grid-${props.width}`}>
      {cells.map((row, i) => row.map((_, j) => {
        if (props.visibleState.host_id == currentUserId) {
          if (j < props.width / 2) {
            return (<UnderCell placeSubmarine={placeSubmarine} key={(i + 1) * (j + 1)} x={i} y={j} className="u-cell" typeString="" images={null} />);
          }
          return (<UnderCell key={(i + 1) * (j + 1)} x={i} y={j} className="u-cell" typeString="nv" images={null} />);
        } if (props.visibleState.visitor_id == currentUserId) {
          if (j < props.width / 2) {
            return (<UnderCell key={(i + 1) * (j + 1)} x={i} y={j} className="u-cell" typeString="nv" images={null} />);
          }
          return (<UnderCell placeSubmarine={placeSubmarine} key={(i + 1) * (j + 1)} x={i} y={j} className="u-cell" typeString="" images={null} />);
        }
      }))}
    </div>
  );
}
