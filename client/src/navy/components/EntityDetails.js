import React from "react";
import "./EntityDetails.css";

const EntityDetails = ({ data, title,game=null}) => {

  

  return (
    <div
      className={`${
        title === "My Ship" || title === "Host" || title === game?.user_1?.username
          ? "my-ship-details"
          : title === "Enemy Ship" || title === "Guest" || title === game?.user_2?.username
          ? "enemy-ship-details"
          : "missile-details"
      } stats-card navy-text rounded`}
    >
      
      <p className="text-center m-0">{title}</p>
      <hr className="m-0"></hr>
      <ul className="stats-list pl-2">
        {Object.keys(data).map((key) => {
          if(key === "user_id"){
            return null
          }
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
