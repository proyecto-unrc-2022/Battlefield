import React from "react";

const Alert = ({ type, text }) => {
  return (
    <div className={"my-1 alert alert-" + type} role="alert">
      {text}
    </div>
  );
};

export default Alert;
