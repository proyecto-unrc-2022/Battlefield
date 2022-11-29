import React, { useState } from "react";
import { Link, useNavigate } from "react-router-dom";
import axios from "axios";
import "./css/style.css";
import authHeader from "../services/auth-header";

export default function UnderHome() {
  const navigate = useNavigate();
  const baseURL = "http://localhost:5000/api/v1/underwater";
  const [alertMessage, setAlertMessage] = useState(null);

  function onClick() {
    axios
      .post(`${baseURL}/game/new`, {}, { headers: authHeader() })
      .then((response) => {
        const sessionId = response.data.session_id;
        navigate(`/underwater/game/${sessionId}`);
      })
      .catch((error) => {
        console.log(error.response.data);
        setAlertMessage(error.response.data.error);
      });
  }

  return (
    <div
      style={{ display: "flex", flexDirection: "column", alignItems: "center" }}
    >
      <div className="u-options">
        <button onClick={onClick} className="u-big-button">
          New Game
        </button>
        <Link to="lobby" className="u-big-button">
          Join Game
        </Link>
      </div>
      {alertMessage != null ? (
        <span className="u-alert-danger">{alertMessage}</span>
      ) : null}
    </div>
  );
}
