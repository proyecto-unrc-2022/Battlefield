import React from "react";
import NavyButton from "../components/NavyButton";
import NavyMenuStars from "../components/NavyMenuStars";
import NavyTitle from "../components/NavyTitle";

const NavyMenu = () => {
  return (
    <div style={{flexGrow: "1"}} className="container-fluid bg-navy">
      <div className="row">
        <div className="col-12 text-center">
          <NavyTitle text="Navy Battleship" size={2}/>
        </div>
      </div>
      <div className="row">
        <div className="col-5 text-center mx-auto mt-3">
          <NavyButton text="Create game" />
          <NavyMenuStars />
          <NavyButton text="join a game" />
          <NavyMenuStars />
          <NavyButton text="how to play" />
        </div>
      </div>
    </div>
  )
};

export default NavyMenu;
