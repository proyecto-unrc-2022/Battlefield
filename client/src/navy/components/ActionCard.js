import React from "react";
import "./ActionCard.css";
import Rudder from "./Rudder";
import attackBtn from "../assets/attack-button.png";
import moveBtn from "../assets/move-button.png";

const ActionCard = ({
  ship,
  changeCourse,
  changeAttack,
  changeMove,
  attack,
  move,
}) => {
  const speed = Array(ship.speed + 1).fill(1);

  const setCourse = (newCourse) => {
    changeCourse(newCourse);
  };

  const handleClickAttack = () => {
    changeAttack();
  };

  const handleClickMove = (quant = 1) => {
    changeMove(parseInt(quant));
  };

  const handleChangeMove = (e) => {
    changeMove(parseInt(e.target.value));
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
            src={attackBtn}
            alt="Attack"
          ></img>
          <p className={"m-0 navy-text " + (attack ? "selected-button" : "")}>
            Attack
          </p>
        </div>
        <div className="col-3 text-center">
          <img
            role={"button"}
            onClick={() => handleClickMove()}
            src={moveBtn}
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
