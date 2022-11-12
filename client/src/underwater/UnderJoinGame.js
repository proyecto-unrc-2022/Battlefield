import React, { useState, useEffect } from "react";
import axios from "axios";
import "./css/style.css"
import authHeader from "../services/auth-header"

const baseURL = "http://127.0.0.1:5000/api/v1/underwater";

function SessionEntry({session}) {
  return (
    <li className="sesion-entry">
      id: {session.id}, 
      host: {session.host_id}
      </li>
  );
}

function GameList() {
  const [sessions, setSessions] = useState([]);

  useEffect(() => {
    axios.get(
      baseURL + "/games",
      {headers: authHeader()}
    ).then(
      (response) => {
        setSessions([]);
        console.log(response.data);
        Object.keys(response.data).map(key => {console.log(response.data[key]); sessions.push(response.data[key])});
      }
    );
  }, []);

  console.log(sessions);

  return (
    <>
      <ul>
        {sessions.map(session => {return <SessionEntry session={session} />;})}
      </ul>
    </>
  );

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
