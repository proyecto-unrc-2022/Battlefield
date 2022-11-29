import React, { useState, useEffect } from "react";
import { Link, useNavigate } from "react-router-dom";
import axios from "axios";
import "./css/style.css";
import authHeader from "../services/auth-header";

const baseURL = "http://127.0.0.1:5000/api/v1/underwater";

function SessionEntry(props) {
  const navigate = useNavigate();
  function sendJoinRequest(event) {
    event.preventDefault();

    axios
      .post(`${baseURL}/game/${props.id}/join`, {}, { headers: authHeader() })
      .then((response) => {
        navigate(`/underwater/game/${props.id}`);
      })
      .catch((error) => {
        console.log(error.response.data);
        props.setAlertMessage(error.response.data.error);
      });
  }

  return (
    <li key={props.id}>
      <span>
        {props.id} - host: {props.session.host.username}
      </span>
      <button onClick={sendJoinRequest} className="u-button u-small-button">
        Join
      </button>
    </li>
  );
}

function GameList({ setAlertMessage, sessions, updateSessionsList }) {
  useEffect(() => {
    updateSessionsList();
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, []);

  return (
    <ul className="u-list">
      {Object.keys(sessions).map((key) => (
        <SessionEntry
          setAlertMessage={setAlertMessage}
          key={key}
          id={key}
          session={sessions[key]}
        />
      ))}
    </ul>
  );
}

export default function UnderJoinGame(props) {
  const [sessions, setSessions] = useState({});
  const [alertMessage, setAlertMessage] = useState(null);

  function updateSessionsList() {
    axios
      .get(`${baseURL}/games`, { headers: authHeader() })
      .then((response) => {
        setSessions(response.data);
      })
      .catch((error) => {
        console.log(error);
      });
  }

  return (
    <div className="u-small-container">
      <h3>Games</h3>
      <GameList
        setAlertMessage={setAlertMessage}
        sessions={sessions}
        updateSessionsList={updateSessionsList}
      />
      <div className="u-input-field">
        <Link to="/underwater/menu" className="u-button">
          ‹
        </Link>
        <button
          onClick={updateSessionsList}
          id="play-button"
          className="u-button"
        >
          Update
        </button>
      </div>
      {alertMessage != null ? (
        <span className="u-alert-danger">{alertMessage}</span>
      ) : null}
    </div>
  );
}
