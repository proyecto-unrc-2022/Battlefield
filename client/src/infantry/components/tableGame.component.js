import React, { Component } from "react";
import "./TableGames.css";

export default class TableGame extends Component {
  constructor(props) {
    super(props);
    this.state = {
      content: null,
    };
  }

  render() {
    const casillas = [];
    for (let i = 0; i < 10; i++) {
      const mapItem = [];
      for (let j = 0; j < 20; j++) {
        if (j === 11 && i === 5)
          mapItem.push(
            <li className="square">
              {" "}
              <div className="projectile"></div>
            </li>
          );
        else mapItem.push(<li className="square"></li>);
      }
      casillas.push(<ul>{mapItem}</ul>);
    }
    return casillas;
  }
}