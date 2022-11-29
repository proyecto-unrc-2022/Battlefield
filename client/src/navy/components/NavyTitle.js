import React from "react";
import "./NavyTitle.css";
import "./../index.css";

const NavyTitle = ({ text, size }) => {
  return <h2 className={`display-${size} navy-text text-uppercase`}>{text}</h2>;
};

export default NavyTitle;
