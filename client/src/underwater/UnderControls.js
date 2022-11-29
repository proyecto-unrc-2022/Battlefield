import React, { useEffect, useState } from "react";
import { useParams } from "react-router-dom";
import axios from "axios";
import authHeader from "../services/auth-header";
import "./css/game-style.css";

export default function UnderControls(props) {
  const [alertMessage, setAlertMessage] = useState(null);
  const params = useParams();
  const sessionId = params.id;
  const gameURL = `http://localhost:5000/api/v1/underwater/game/${sessionId}`;

  function DirectionControl(props) {
    const rotation = 45 * props.position.direction;

    const style = {
      transform: `rotate(${rotation}deg)`,
    };

    function setDirection(dir) {
      props.setPosition({
        x: props.position.x,
        y: props.position.y,
        direction: dir,
      });
    }

    const array1 = [7, 0, 1, 6];
    const array2 = [2, 5, 4, 3];

    return (
      <div style={{ position: "relative", height: 157, width: 157 }}>
        <img
          alt="direction-compass"
          style={style}
          className="u-overlap-1"
          src={require("./css/images/direc.png")}
          width="100%"
        />
        <div className="u-overlap-2 u-direction-grid">
          {array1.map((i) => (
            <div
              key={i}
              style={{ height: "100%", width: "100%" }}
              onClick={(_) => setDirection(i)}
            />
          ))}
          <div style={{ height: "100%", width: "100%" }} />
          {array2.map((i) => (
            <div
              key={i}
              style={{ height: "100%", width: "100%" }}
              onClick={(_) => setDirection(i)}
            />
          ))}
        </div>
      </div>
    );
  }

  function AdvanceControl() {
    const [steps, setSteps] = useState(0);

    function advance(event) {
      event.preventDefault();

      const headers = authHeader();
      headers["Content-Type"] = "application/json";
      axios
        .post(
          `${gameURL}/rotate_and_advance`,
          {
            direction: props.position.direction,
            steps: parseInt(steps),
          },
          { headers }
        )
        .then((_) => console.log("Submarine advance"))
        .catch((error) => {
          console.log(error.response.data);
          setAlertMessage(error.response.data.error);
        });
    }

    const style = {
      display: "flex",
      gap: "20px",
      alignItems: "center",
    };

    return (
      <div style={style}>
        <div onClick={advance} className="u-control-button" title="advance">
          <img
            alt="advance"
            src={require("./css/buttons/advancebutton.png")}
            width="60"
            height="60"
          />
        </div>
        <input
          className="u-number-input"
          type="number"
          min="0"
          value={steps}
          onChange={(event) => {
            setSteps(event.target.value);
          }}
        />
      </div>
    );
  }

  function ActionButtons() {
    function skip() {
      // Implemented as advancing 0 steps
      const headers = authHeader();
      headers["Content-Type"] = "application/json";
      axios
        .post(
          `${gameURL}/rotate_and_advance`,
          {
            direction: props.visibleState.submarine.direction,
            steps: 0,
          },
          { headers }
        )
        .then((_) => console.log("Skipped this turn"))
        .catch((error) => {
          console.log(error.response.data);
          setAlertMessage(error.response.data.error);
        });
    }

    function useRadar() {
      axios
        .post(`${gameURL}/send_radar_pulse`, {}, { headers: authHeader() })
        .then((_) => console.log("Radar pulse command sent"))
        .catch((error) => {
          console.log(error.response.data);
          setAlertMessage(error.response.data.error);
        });
    }

    function attack() {
      const headers = authHeader();
      headers["Content-Type"] = "application/json";
      axios
        .post(
          `${gameURL}/rotate_and_attack`,
          { direction: props.position.direction },
          { headers }
        )
        .then((_) => {
          console.log("Attack command sent");
        })
        .catch((error) => {
          console.log(error.response.data);
          setAlertMessage(error.response.data.error);
        });
    }

    function surrender() {
      axios
        .post(
          `${gameURL}/leave`,
          {},
          {
            headers: authHeader(),
          }
        )
        .then((_) => console.log("leaving game"));
    }

    return (
      <>
        <div
          id="surrender"
          className="u-control-button"
          onClick={surrender}
          title="🐔"
        >
          <img
            alt="surrender"
            src={require("./css/buttons/surrenderbutton.png")}
            width="40"
            height="40"
          />
        </div>
        <div className="u-control-button" onClick={skip} title="skip">
          <img
            alt="skip"
            src={require("./css/buttons/skipbutton.png")}
            width="60"
            height="60"
          />
        </div>
        <div
          className="u-control-button"
          onClick={useRadar}
          title="radar pulse"
        >
          <img
            alt="radar"
            src={require("./css/buttons/radarbutton.png")}
            width="60"
            height="60"
          />
        </div>
        <div className="u-control-button" onClick={attack} title="attack">
          <img
            alt="attack"
            src={require("./css/buttons/missilebutton.png")}
            width="60"
            height="60"
          />
        </div>
      </>
    );
  }

  useEffect(
    (_) => {
      setAlertMessage(null);
    },
    [props.visibleState]
  );

  return (
    <div style={{ display: "flex", flexDirection: "column", width: "100%" }}>
      <div className="u-controls-container">
        <div className="u-left-controls">
          <DirectionControl
            position={props.position}
            setPosition={props.setPosition}
          />
          <AdvanceControl />
        </div>
        <div className="u-right-controls">
          <ActionButtons />
        </div>
      </div>
      <div>
        {alertMessage != null ? (
          <p className="u-alert-danger">{alertMessage}</p>
        ) : null}
      </div>
    </div>
  );
}
