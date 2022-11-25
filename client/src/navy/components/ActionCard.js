import React, { useState } from "react";
import "./ActionCard.css";
import Rudder from "./Rudder";
import attackButton from "../assets/attack-button.png";
import moveButton from "../assets/move-button.png";

const ActionCard = ({ ship, changeCourse, changeAttack, changeMove }) => {
  const speed = Array(ship.speed + 1).fill(1);
  const [move, setMove] = useState(false);
  const [attack, setAttack] = useState(false);

  const setCourse = (newCourse) => {
    changeCourse(newCourse);
  };

  const handleClickAttack = () => {
    setMove(false);
    setAttack(true);
    changeAttack();
  };

  const handleClickMove = (quant) => {
    setMove(true);
    setAttack(false);
    changeMove(parseInt(quant));
  };

  const handleChangeMove = (e) => {
    setMove(true);
    setAttack(false);
    changeMove(parseInt(e.target.value));
  };

  const effectMouseEnterHover = (e) => {
    e.target.style.cursor = "pointer";
  };

  return (
    <div className="action-card p-3 rounded">
      <div className="row align-items-center">
        <div className="col-4">
          <Rudder ship={ship} changeCourse={setCourse} />
        </div>
        <div className="col-3 text-center">
          <img
            role={"button"}
            onClick={handleClickAttack}
            src={attackButton}
            alt="Attack"
          ></img>
          <p className={"m-0 navy-text " + (attack ? "selected-button" : "")}>
            Attack
          </p>
        </div>
        <div className="col-3 text-center">
          <img
            role={"button"}
            onClick={() => handleClickMove(0)}
            src={moveButton}
            alt="Move"
          ></img>
          <p className={"m-0 navy-text " + (move ? "selected-button" : "")}>
            Move
          </p>
        </div>
        {move ? (
          <div className="col-2 text-center">
            {speed.map((el, i) => {
              return (
                <div key={i} className="d-flex justify-content-around">
                  <input
                    onChange={handleChangeMove}
                    id={i}
                    value={i}
                    name="move"
                    type="radio"
                  />
                  <label className="m-0 navy-text mr-2" htmlFor={i}>
                    {i}
                  </label>
                </div>
              );
            })}
          </div>
        ) : null}
      </div>
    </div>
  );
};

export default ActionCard;
