import React, { useState } from "react";
import "./ActionCard.css";
import Rudder from "./Rudder";
import attackButton from "../assets/attack-button.png";
import moveButton from "../assets/move-button.png";

const ActionCard = () => {
  const [move, setMove] = useState(false);
  return (
    <div className="action-card p-3">
      <div className="row align-items-center">
        <div className="col-4">
          <Rudder />
        </div>
        <div className="col-3 text-center">
          <img onClick={() => setMove(false)} src={attackButton} alt="Attack"></img>
          <p className="m-0">Attack</p>
        </div>
        <div className="col-3 text-center">
          <img onClick={() => setMove(true)} src={moveButton} alt="Move"></img>
          <p className="m-0">Move</p>
        </div>
        {move ? (
          <div className="col-2 text-center">
            <div className="d-flex">
              <label className="m-0" htmlFor="1">
                1
              </label>
              <input id="1" value={1} name="move" type="radio" />
            </div>
            <div className="d-flex">
              <label className="m-0" htmlFor="2">
                2
              </label>
              <input id="2" value={2} name="move" type="radio" />
            </div>
            <div className="d-flex">
              <label className="m-0" htmlFor="3">
                3
              </label>
              <input id="3" value={3} name="move" type="radio" />
            </div>
            <div className="d-flex">
              <label className="m-0" htmlFor="4">
                4
              </label>
              <input id="4" value={4} name="move" type="radio" />
            </div>
          </div>
        ) : null}
      </div>
    </div>
  );
};

export default ActionCard;
