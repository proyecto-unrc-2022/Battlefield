import React from "react";
import "./EntityDetails.css";

const EntityDetails = ({ data, title }) => {
  return (
    <div
      className={`${
        title === "My Ship" || title === "Host"
          ? "my-ship-details"
          : title === "Enemy Ship" || title === "Guest"
          ? "enemy-ship-details"
          : "missile-details"
      } stats-card navy-text rounded`}
    >
      <p className="text-center m-0">{title}</p>
      <hr className="m-0"></hr>
      <ul className="stats-list pl-2">
        {Object.keys(data).map((key) => {
          return (
            <li key={key}>
              {`${key}
             : ${data[key]}`}
            </li>
          );
        })}
      </ul>
    </div>
  );
};

export default EntityDetails;
