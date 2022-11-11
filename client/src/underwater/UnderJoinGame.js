import React, { useState, useEffect } from "react";
import axios from "axios";
import "./css/style.css"
import authHeader from "../services/auth-header"

const baseURL = "http://127.0.0.1:5000/api/v1/underwater";

function GameList() {
  const [games, setGames] = useState([]);

  useEffect(() => {
    axios.get(
      baseURL + "/games",
      {headers: authHeader()}
    ).then(
      (response) => {
        setGames([]);
        Object.keys(response.data).forEach(key => {games.push(response.data[key]);});
        console.log(games);
      }
    );
  }, [])

  return (
    <ul></ul>
    )

}

export default function JoinGame(props) {
  return (
    <div className="u-small-container">
      <div className="row"><h3>Games</h3></div>
      <form>
        <div className="row u-input-field">
          <GameList />
          <div onClick={() => {props.setVisibleComp("home")}} className="u-button">‹</div>
        </div>
      </form>
    </div>
    )
}
