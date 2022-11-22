import { useState, useEffect } from "react";
import axios from "axios";
import "./css/game-style.css"

const optionsURL = "http://127.0.0.1:5000/api/v1/underwater/game/submarine_options";

function SubmarineCard({id, setChosenSubmarine, stats}) {
  const onClick = () => {
    setChosenSubmarine(parseInt(id));
  }

  return (
    <a onClick={onClick} id={id} href="#"><div className="card">
      <img src="https://static-s.aa-cdn.net/img/ios/1451817911/973e1c13fd06634d7de878a801664cc5?v=1" alt="Submarine" />
      <ul>
        <li><strong>{stats.name}</strong></li>
        <li>Size: {stats.size}</li>
        <li>Speed: {stats.speed}</li>
        <li>visibility: {stats.visibility}</li>
        <li>radar_scope: {stats.radar_scope}</li>
        <li>health: {stats.health}</li>
        <li>torpedo_speed: {stats.torpedo_speed}</li>
        <li>torpedo_damage: {stats.torpedo_damage}</li>
      </ul>
    </div></a>
  );
}

export default function ChooseSubmarine({setChosenSubmarine}) {
  const [options, setOptions] = useState(null);

  useEffect(() => {
    axios.get(optionsURL).then(response => { setOptions(response.data); })
      .catch(error => {console.log(error);});
  }, []);

  return (
    <div className="u-choose-submarine">
      <div className="cards-container">
        {options != null ? Object.keys(options).map(key => {return <SubmarineCard key={key} id={key} setChosenSubmarine={setChosenSubmarine} stats={options[key]} />}) : null}
      </div>
    </div>
  );
}
