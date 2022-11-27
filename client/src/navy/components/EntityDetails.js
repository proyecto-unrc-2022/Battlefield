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
      <hr></hr>
      <ul className="stats-list pl-2">
        {Object.keys(data).map((key) => {
          let temp = key
          if (key === "hp"){
            if(data[key] == 0){
              temp = "Destroyed ☠☠"
            }
            if(data[key] < 20){
              temp = "❤"
            }
            else if(data[key] < 50 ){

              temp = "❤❤" 
            }
            else if(data[key] > 50){
              temp = "❤❤❤"
            }

          }

          return <li key={key}>
            
            {`${temp}
             : ${data[key]}`}
            </li>;
        })}
      </ul>
    </div>
  );
};

export default EntityDetails;
