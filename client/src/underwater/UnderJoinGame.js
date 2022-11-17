import React, { useState, useEffect } from "react";
import axios from "axios";
import "./css/style.css"
import authHeader from "../services/auth-header"

const baseURL = "http://127.0.0.1:5000/api/v1/underwater";

function SessionEntry(props) {
  function sendJoinRequest(event) {
    event.preventDefault();

    axios.post(
      baseURL + "/game/" + props.id + "/join",
      {},
      {headers: authHeader()}
    ).then(response => {
      ; 
    }).catch(error => {
      console.log(error.response.data);
      props.setAlertMessage(error.response.data["error"]);
    });
  }

  return (
    <li key={props.id}>
      <span>
        id: {props.id}, 
        host: {props.session.host_id}
      </span>
      <form onSubmit={sendJoinRequest}>
        <button type="submit" className="u-button u-small-button">Join</button>
      </form>
    </li>
    );
}

function GameList({setAlertMessage, sessions, updateSessionsList}) {
  useEffect(() => {
    updateSessionsList();
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, []);

  return (
    <div className="row u-input-field">
      <ul className="u-list">
        {Object.keys(sessions).map(key => {return <SessionEntry setAlertMessage={setAlertMessage} key={key} id={key} session={sessions[key]} />;})}
      </ul>
    </div>
    );

}

export default function JoinGame(props) {
  const [sessions, setSessions] = useState({});
  const [alertMessage, setAlertMessage] = useState(null);

  function updateSessionsList() {
    axios.get(
      baseURL + "/games",
      {headers: authHeader()}
    ).then(
      (response) => { setSessions(response.data); }
    ).catch((error) => {console.log(error);});
  }

  return (
    <div className="u-small-container">
      <div className="row"><h3>Games</h3></div>
      <div className="row">
        <GameList setAlertMessage={setAlertMessage} sessions={sessions} updateSessionsList={updateSessionsList} />
      </div>
      <div className="row u-input-field">
        <div onClick={() => {props.setVisibleComp("home")}} className="u-button">‹</div>
        <div onClick={updateSessionsList} id="play-button" className="u-button">Update</div>
      </div>
      {alertMessage != null ? <span className="alert-danger">{alertMessage}</span> : null}
    </div>
    )
}
