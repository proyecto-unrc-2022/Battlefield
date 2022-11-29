import React from "react";
import user from "../assets/user-icon.svg";
import eagle from "../assets/eagle.png";
import "./NavyUserCard.css";

const NavyUserCard = ({ username, rol = "host" }) => {
  const styles = {
    host: {
      backgroundColor: "#2DA0ED",
      boxShadow: "inset 0px 0px 30px #0F0F0F",
    },
    guest: {
      backgroundColor: "#E57C7C",
      boxShadow: "inset 0px 0px 30px #0F0F0F",
    },
    free: {
      backgroundColor: "#9EAEBE",
      boxShadow: "inset 0px 0px 30px #0F0F0F",
    },
  };

  return (
    <div style={styles[rol]} className="h-100 border border-dark">
      <div className="navy-user-card border border-bottom-0 border-dark p-1">
        <div className="border border-dark rounded p-2 text-center">
          <img src={user} alt="User" />
        </div>
        <div className="text-center">
          <img className="w-75" src={eagle} alt="Eagle" />
        </div>
      </div>
      <div className="w-100 border border-dark navy-user-card">
        <div className="px-2">
          {username ? (
            <p
              style={{ fontSize: "0.8rem", overflow: "hidden" }}
              className="m-0 text-center navy-text"
            >
              {username}
            </p>
          ) : (
            <p
              style={{
                fontSize: "0.8rem",
                overflow: "hidden",
                color: "transparent",
              }}
              className="m-0 text-center navy-text"
            >
              Username
            </p>
          )}
        </div>
      </div>
    </div>
  );
};

export default NavyUserCard;
