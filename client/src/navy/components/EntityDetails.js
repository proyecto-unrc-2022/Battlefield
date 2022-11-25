import React from "react";
import "./EntityDetails.css";

const EntityDetails = ({ data, title }) => {
  return (
    <div
      className={`${
        title === "My Ship"
          ? "my-ship-details"
          : title === "Enemy Ship"
          ? "enemy-ship-details"
          : "missile-details"
      } stats-card navy-text rounded`}
    >
      <p className="text-center m-0">{title}</p>
      <hr></hr>
      <ul className="stats-list pl-2">
        {Object.keys(data).map((key) => {
          return <li key={key}>{`${key} : ${data[key]}`}</li>;
        })}
      </ul>
    </div>
  );
};

export default EntityDetails;
