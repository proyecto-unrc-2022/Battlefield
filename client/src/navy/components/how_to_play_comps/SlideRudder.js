import React, { useState } from "react";
import "../Rudder.css";
import rudder from "../../assets/rudder.png";

const SlideRudder = ({ changeCourse }) => {
  const [course, setCourse] = useState(" ");

  const handleShipCourse = (e) => {
    setCourse(e.target.ariaValueText);
    changeCourse(e.target.ariaValueText);
  };

  return (
    <>
      <div className="row">
        <div
          role={"button"}
          onClick={handleShipCourse}
          aria-valuetext="NW"
          className={
            "col-4 d-flex justify-content-center align-items-center navy-text " +
            (course === "NW" ? "selected-course" : "")
          }
        >
          NW
        </div>
        <div
          role={"button"}
          onClick={handleShipCourse}
          aria-valuetext="N"
          className={
            "col-4 d-flex justify-content-center align-items-center navy-text " +
            (course === "N" ? "selected-course" : "")
          }
        >
          N
        </div>
        <div
          role={"button"}
          onClick={handleShipCourse}
          aria-valuetext="NE"
          className={
            "col-4 d-flex justify-content-center align-items-center navy-text " +
            (course === "NE" ? "selected-course" : "")
          }
        >
          NE
        </div>
      </div>
      <div className="row">
        <div
          role={"button"}
          onClick={handleShipCourse}
          aria-valuetext="W"
          className={
            "col-3 d-flex justify-content-center align-items-center navy-text " +
            (course === "W" ? "selected-course" : "")
          }
        >
          W
        </div>
        <div className="col-6 d-flex justify-content-center align-items-center">
          <img className="w-100 h-auto" src={rudder} alt="rudder"></img>
        </div>
        <div
          role={"button"}
          onClick={handleShipCourse}
          aria-valuetext="E"
          className={
            "col-3 d-flex justify-content-center align-items-center navy-text " +
            (course === "E" ? "selected-course" : "")
          }
        >
          E
        </div>
      </div>
      <div className="row">
        <div
          role={"button"}
          onClick={handleShipCourse}
          aria-valuetext="SW"
          className={
            "col-4 d-flex justify-content-center align-items-center navy-text " +
            (course === "SW" ? "selected-course" : "")
          }
        >
          SW
        </div>
        <div
          role={"button"}
          onClick={handleShipCourse}
          aria-valuetext="S"
          className={
            "col-4 d-flex justify-content-center align-items-center navy-text " +
            (course === "S" ? "selected-course" : "")
          }
        >
          S
        </div>
        <div
          role={"button"}
          onClick={handleShipCourse}
          aria-valuetext="SE"
          className={
            "col-4 d-flex justify-content-center align-items-center navy-text " +
            (course === "SE" ? "selected-course" : "")
          }
        >
          SE
        </div>
      </div>
    </>
  );
};

export default SlideRudder;
