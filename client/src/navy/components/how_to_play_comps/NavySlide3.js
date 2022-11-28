import GridShipPlace from "../GridShipPlace";
import React, { useState } from "react";
import "../GridShipPlace.css";

const NavySlide3 = () => {
  const position = { x: 5, y: 5 };
  const [course, setCourse] = useState("N");

  const handleChangeCourse = (e) => {
    setCourse(e.target.value);
  };

  return (
    <div className="text-break">
      <p className="text-justify">
        Then the ship must be placed, with the initial coordinates and course.
        It should be noted that the ship cannot be initially placed outside the
        grid. Notice that each user places the ship in different halves of the
        board.
      </p>
      <div className="d-flex">
        <p className="navy-text m-0 mr-1">Course:</p>
        <select
          onChange={handleChangeCourse}
          className="custom-select custom-select-sm"
          style={{ width: "50px" }}
        >
          <option value={"N"}>N</option>
          <option value={"S"}>S</option>
          <option value={"E"}>E</option>
          <option value={"W"}>W</option>
          <option value={"NE"}>NE</option>
          <option value={"NW"}>NW</option>
          <option value={"SE"}>SE</option>
          <option value={"SW"}>SW</option>
        </select>
      </div>
      <div className="row mx-auto mt-3 ">
        <GridShipPlace
          course={course}
          cols={20}
          rows={10}
          size={3}
          selectPosition={position}
        />
      </div>
    </div>
  );
};

export default NavySlide3;
