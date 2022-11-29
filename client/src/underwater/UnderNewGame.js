import React, { useState } from "react";
import { Link, useNavigate } from "react-router-dom";
import axios from "axios";
import authHeader from "../services/auth-header";

const baseURL = "http://127.0.0.1:5000/api/v1/underwater";

export default function UnderNewGame(props) {
  const navigate = useNavigate();
  const [height, setHeight] = useState(10);
  const [width, setWidth] = useState(20);
  const [alertMessage, setAlertMessage] = useState(null);

  function onSubmit(e) {
    e.preventDefault();

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
    <div className="u-small-container">
      <form onSubmit={onSubmit}>
        <div className="row">
          <div className="u-input-field">
            <label htmlFor="height">Height</label>
            <input
              type="range"
              min="10"
              max="20"
              step="2"
              id="height"
              value={height}
              onChange={(event) => setHeight(event.target.value)}
            />
            <span style={{ marginLeft: "8px" }}>{height}</span>

            <label htmlFor="width">Width</label>
            <input
              type="range"
              min="20"
              max="40"
              step="2"
              id="width"
              value={width}
              onChange={(event) => setWidth(event.target.value)}
            />
            <span style={{ marginLeft: "8px" }}>{width}</span>
          </div>

          <div className="u-input-field">
            <label className="inline-block" htmlFor="players">
              Players
            </label>
            <select type="select" id="players">
              <option value="2">2</option>
              <option value="4">4</option>
            </select>
          </div>
        </div>

        <div className="row u-input-field">
          <Link to="/underwater/menu" className="u-button">
            ‹
          </Link>
          <button id="play-button" className="u-button">
            Play
          </button>
        </div>
        {alertMessage != null ? (
          <span className="u-alert-danger">{alertMessage}</span>
        ) : null}
      </form>
    </div>
  );
}
