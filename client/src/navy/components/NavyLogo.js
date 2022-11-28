import React from "react";
import { useNavigate } from "react-router-dom";
import "./../index.css";
import left_wing from "../assets/left_wing.svg";
import right_wing from "../assets/right_wing.svg";
import "./NavyButton.css";
import "./NavyLogo.css";

const NavyLogo = ({ size, role }) => {
  const navigate = useNavigate();

  const goToMenu = () => {
    navigate("/navy");
  };

  return (
    <div
      role={"button"}
      onClick={goToMenu}
      className={`navy-logo navy-text navy-button-${size} mt-1 mx-2`}
    >
      <img src={right_wing} alt="" className={`navy-logo-wing`} />
      {"Navy Battleship"}
      <img src={left_wing} alt="" className={`navy-logo-wing`} />
    </div>
  );
};

export default NavyLogo;
