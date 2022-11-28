import React from "react";
import "./Modal.css";

const Modal = ({ children, isOpen }) => {
  return (
    <div className={"modal " + (isOpen ? "is-open" : "")}>
      <div className="modal-container">{children}</div>
    </div>
  );
};

export default Modal;
