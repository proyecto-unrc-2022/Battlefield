import { useState, useEffect } from "react";
import axios from "axios";
import "./css/game-style.css";

const optionsURL =
  "http://localhost:5000/api/v1/underwater/game/submarine_options";

function SubmarineCard({ id, setChosenSubmarine, stats }) {
  const onClick = () => {
    setChosenSubmarine(parseInt(id));
  };

  function PercentageBar(props) {
    const { stat, max, value } = props;
    const percentage = (value / max) * 100;

    return (
      <div className="u-bar-100">
        <div className="u-stat-bar" style={{ width: `${percentage}%` }} />
        <div className="u-stat-bar-text">
          <span style={{ fontSize: "13px" }}>{stat}</span>
          <span style={{ fontSize: "13px" }}>{value}</span>
        </div>
      </div>
    );
  }

  return (
    <div className="u-card">
      <a onClick={onClick} id={id} href="#">
        <div style={{ width: "100%", backgroundColor: "#FFF" }}>
          <img
            src={require(`./css/images/submarine${id}Preview.png`)}
            alt="Submarine"
          />
          <strong style={{ fontSize: "13px", height: "20px" }}>
            {stats.name}
          </strong>
          <div className="u-bars-container">
            <PercentageBar stat="health" max={80} value={stats.health} />
            <PercentageBar stat="size" max={4} value={stats.size} />
            <PercentageBar stat="speed" max={5} value={stats.speed} />
            <PercentageBar stat="visibility" max={5} value={stats.visibility} />
            <PercentageBar
              stat="radar scope"
              max={15}
              value={stats.radar_scope}
            />
            <PercentageBar
              stat="torpedo speed"
              max={5}
              value={stats.torpedo_speed}
            />
            <PercentageBar
              stat="torpedo damage"
              max={25}
              value={stats.torpedo_damage}
            />
          </div>
        </div>
      </a>
    </div>
  );
}

export default function ChooseSubmarine({ setChosenSubmarine }) {
  const [options, setOptions] = useState(null);

  useEffect(() => {
    axios
      .get(optionsURL)
      .then((response) => {
        setOptions(response.data);
      })
      .catch((error) => {
        console.log(error);
      });
  }, []);

  return (
    <div className="u-cards-container">
      {options != null
        ? Object.keys(options).map((key) => (
            <SubmarineCard
              key={key}
              id={key}
              setChosenSubmarine={setChosenSubmarine}
              stats={options[key]}
            />
          ))
        : null}
    </div>
  );
}
