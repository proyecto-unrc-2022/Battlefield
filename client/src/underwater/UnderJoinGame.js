import React, { useState, useEffect } from "react";
import axios from "axios";
import "./css/style.css"
import authHeader from "../services/auth-header"

const baseURL = "http://127.0.0.1:5000/api/v1/underwater";

function SessionEntry({id, session}) {
  return (
    <li key={id}>
      <span>
        id: {id}, 
        host: {session.host_id}
      </span>
      <button className="u-button u-small-button">Join</button>
    </li>
    );
}

function GameList() {
  const [sessions, setSessions] = useState({});

  function updateSessionsList() {
    axios.get(
      baseURL + "/games",
      {headers: authHeader()}
    ).then(
      (response) => { setSessions(response.data); }
    );
  }

  useEffect(() => {updateSessionsList();}, []);

  return (
    <div className="row u-input-field">
      <ul className="u-list">
        {Object.keys(sessions).map(key => {return <SessionEntry id={key} session={sessions[key]} />;})}
      </ul>
    </div>
    );

}

export default function JoinGame(props) {
  return (
    <div className="u-small-container">
      <div className="row"><h3>Games</h3></div>
      <form>
        <div className="row">
          <GameList />
        </div>
        <div className="row u-input-field">
          <div onClick={() => {props.setVisibleComp("home")}} className="u-button">‹</div>
          <button id="play-button" className="u-button">Update</button>
        </div>
      </form>
    </div>
    )
}
