import React from "react";
import "./EntityDetails.css";

const EntityDetails = ({ data, title }) => {
  return (
    <div className={`${title} stats-card`}>
      <p>{title}</p>
      <hr></hr>
      <ul className="stats-list">
        {Object.keys(data).map((key) => {
          return <li key={key}>{`${key} : ${data[key]}`}</li>;
        })}
      </ul>
    </div>
  );
};

export default EntityDetails;
