import React, { useState, useEffect } from "react";
import { useParams, useNavigate } from "react-router-dom";
import axios from "axios";
import authHeader from "../services/auth-header";
import ChooseSubmarine from "./ChooseSubmarine";
import PlaceSubmarine from "./PlaceSubmarine";
import UnderBoard from "./UnderBoard";
import UnderControls from "./UnderControls";
import UnderLoading from "./UnderLoading";
import UnderStats from "./UnderStats";
import "./css/style.css";
import "./css/game-style.css";
import authService from "../services/auth.service";

export default function UnderGame() {
  const params = useParams();
  const navigate = useNavigate();
  const width = 20;
  const height = 10;
  const sessionId = params.id;
  const currentUserId = authService.getCurrentUser().sub;
  const [roomIsFull, setRoomIsFull] = useState(false);
  const [chosenSubmarine, setChosenSubmarine] = useState(null);
  const [position, setPosition] = useState(null);
  const [layout, setLayout] = useState(null);
  const [requestWasSent, setRequestWasSent] = useState(false);
  const [visibleState, setVisibleState] = useState(null);
  const [winnerId, setWinnerId] = useState(null);
  const [winner, setWinner] = useState(null);
  const URL = `http://localhost:5000/api/v1/underwater/game/${sessionId}`;

  useEffect(
    (_) => {
      const sse = new EventSource(`${URL}/listen`);

      sse.onmessage = (e) => {
        const data = JSON.parse(e.data);
        console.log("Message received:", data);
        if (data.message === "joined") setRoomIsFull(true);
        else if (
          data.message === "moved" ||
          data.message === "submarine placed" ||
          data.message === "torpedos moved"
        )
          updateVisibleState();
        else if (data.winner_id !== undefined) {
          console.log("Game ended");
          setWinnerId(data.winner_id);
        }
      };

      updateVisibleState();
      return (_) => sse.close();
    },
    [URL]
  );

  useEffect(
    (_) => {
      if (visibleState !== null && winnerId !== null)
        setWinner(
          winnerId === visibleState.host_id
            ? visibleState.host
            : visibleState.visitor
        );
    },
    [visibleState, winnerId]
  );

  useEffect(
    (_) => {
      if (winner != null) endGame();
    },
    [winner]
  );

  function endGame() {
    if (visibleState.host_id === currentUserId) {
      // So that only the host sends a delete request
      axios
        .post(`${URL}/delete`, {}, { headers: authHeader() })
        .then((_) => console.log("Game deleted"));
    }
  }

  function ShowWinner({ winner }) {
    function onClick() {
      navigate("/underwater/menu");
    }
    const style = {
      color: "white",
      display: "flex",
      flexDirection: "column",
      height: "450px",
      width: "100%",
      alignItems: "center",
      justifyContent: "center",
      gap: "20px",
    };

    return (
      <div style={style}>
        <h1>¡{winner.username} won!</h1>
        <button className="u-button" onClick={onClick}>
          Back to menu
        </button>
      </div>
    );
  }

  function sendChooseSubmarine() {
    const headers = authHeader();
    headers["Content-Type"] = "application/json";
    axios
      .post(
        `${URL}/choose_submarine`,
        {
          submarine_id: chosenSubmarine,
          x_position: position.x,
          y_position: position.y,
          direction: position.direction,
        },
        { headers }
      )
      .then((_) => console.log("Submarine chosen"));
  }

  function updateVisibleState() {
    if (winner != null) return;
    axios.get(URL, { headers: authHeader() }).then((response) => {
      console.log("Setting visible state", response.data);
      setVisibleState(response.data);

      if (response.data.visitor_id != null) setRoomIsFull(true);
    });
  }

  useEffect(
    (_) => {
      if (winner !== null)
        setLayout({ main: <ShowWinner winner={winner} />, bottom: null });
      else if (roomIsFull) {
        if (chosenSubmarine == null) {
          setLayout({
            main: <ChooseSubmarine setChosenSubmarine={setChosenSubmarine} />,
            bottom: <h1 style={{ marginTop: "20px" }}>Choose your fighter</h1>,
          });
        } else if (position == null) {
          setLayout({
            main: (
              <PlaceSubmarine
                visibleState={visibleState}
                setPosition={setPosition}
                width={width}
                height={height}
              />
            ),
            bottom: <h1 style={{ marginTop: "20px" }}>Place your submarine</h1>,
          });
        } else {
          if (!requestWasSent) {
            sendChooseSubmarine();
            setRequestWasSent(true);
          }
          setLayout({
            main: (
              <UnderBoard
                visibleState={visibleState}
                width={width}
                height={height}
              />
            ),
            bottom: (
              <>
                <UnderStats
                  visibleState={visibleState}
                  currentUserId={currentUserId}
                />
                <UnderControls
                  visibleState={visibleState}
                  position={position}
                  setPosition={setPosition}
                />
              </>
            ),
          });
        }
      }
    },
    [currentUserId, chosenSubmarine, position, visibleState, roomIsFull, winner]
  );

  return (
    <div className="u-container">
      <div className="u-game-container">
        <div className="u-screen">
          {layout == null ? <UnderLoading /> : layout.main}
        </div>
        <div className="u-bottom-div">
          {layout == null ? null : layout.bottom}
        </div>
      </div>
    </div>
  );
}
