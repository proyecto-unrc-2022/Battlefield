import React from "react";
import "./NavyButton.css";
import "./../index.css";

const NavyButton = ({ text, size, styles = {}, action }) => {
  return (
    <div
      role={"button"}
      onClick={action}
      style={{ ...styles }}
      className={`navy-button navy-button-${size} rounded border border-dark text-uppercase navy-text my-1`}
      id="pruebita"
    >
      {text}
    </div>
  );
};

export default NavyButton;
