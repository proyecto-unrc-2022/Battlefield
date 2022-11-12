import React, { useEffect, useState } from "react";
import wings from "./../assets/wings.svg";
import NavyButton from "./NavyButton";
import NavyUserCard from "./NavyUserCard";
import UserService from "../../services/user.service";
import "./NavyGameCard.css";
import authService from "../../services/auth.service";

const NavyGameCard = ({ game }) => {
  const [user1, setUser1] = useState({})
  const [user2, setUser2] = useState({})

  const canJoin = () => {
    const currentUser = authService.getCurrentUser();
    return currentUser.sub !== game.user_1.id && (Object.keys(user2).length === 0)
  }

  const canReJoin = () => {
    const currentUser = authService.getCurrentUser();
    return currentUser.sub === game.user_1.id || currentUser.sub === game.user_2.id
  }

  useEffect(() => {
    if (game.user_2){
      setUser2(game.user_2)
    }
  }, [])

  return (
    <div className="navy-card-container d-flex flex-column align-items-center border border-dark pt-2 pb-4">
      <p className="navy-text m-0">{game.id}</p>
      <div className="w-100 d-flex justify-content-center mb-2">
        <img src={wings} alt="Wings" />
      </div>
      <div className="w-75 d-flex justify-content-around align-items-center">
        <NavyUserCard username={game.user_1.username} />
        <p className="navy-text">VS.</p>
        <NavyUserCard username={(Object.keys(user2).length !== 0) ? user2.username : ""} rol={(Object.keys(user2).length !== 0) ? "guest" : "free"}/>
      </div>
      {canJoin() ? (
        <div className="text-center">
          <NavyButton text={"join"} size={"small"} />
        </div>
      ) : null}
    </div>
  );
};

export default NavyGameCard;
