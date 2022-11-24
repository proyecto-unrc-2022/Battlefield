import React from "react";
import "./Rudder.css";
import rudder  from "../assets/rudder.png";

const Rudder = () => {
  return (
    <>
      <div className="row">
        <div className="col-4 d-flex justify-content-center align-items-center">NW</div>
        <div className="col-4 d-flex justify-content-center align-items-center">N</div>
        <div className="col-4 d-flex justify-content-center align-items-center">NE</div>
      </div>
      <div className="row">
        <div className="col-3 d-flex justify-content-center align-items-center">W</div>
        <div className="col-6 d-flex justify-content-center align-items-center">
          <img className="w-100 h-auto" src={rudder} alt="rudder"></img>
        </div>
        <div className="col-3 d-flex justify-content-center align-items-center">E</div>
      </div>
      <div className="row">
        <div className="col-4 d-flex justify-content-center align-items-center">SW</div>
        <div className="col-4 d-flex justify-content-center align-items-center">S</div>
        <div className="col-4 d-flex justify-content-center align-items-center">SE</div>
      </div>
    </>
  );
};

export default Rudder;
