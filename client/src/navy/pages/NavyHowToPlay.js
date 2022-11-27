import React from "react";
import NavyLogo from "../components/NavyLogo";
import NavyTitle from "../components/NavyTitle";
import NavySlider from "../components/how_to_play_comps/NavySlider";

const NavyHowToPlay = () => {
  return (
    <div style={{ flexGrow: "1" }} className="container-fluid bg-navy">
      <div className="row justify-content-between p-2 align-items-center">
        <NavyLogo size={"small"} />
      </div>
      <div className="row">
        <div className="col-12 text-center">
          <NavyTitle text={"How To Play"} size={4} />
        </div>
      </div>
      <div className="row justify-content-center text-center mt-4">
        <NavySlider />
      </div>
    </div>
  );
};

export default NavyHowToPlay;
