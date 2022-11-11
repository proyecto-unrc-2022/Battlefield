import React, { useEffect, useState } from "react";
import wings from "./../assets/wings.svg";
import NavyButton from "./NavyButton";
import NavyUserCard from "./NavyUserCard";
import UserService from "../../services/user.service";
import "./NavyGameCard.css";
import authService from "../../services/auth.service";

const NavyGameCard = ({ game }) => {
  const [user1, setUser1] = useState({});
  const [user2, setUser2] = useState({});

  const canJoin = () => {
    const currentUser = authService.getCurrentUser();
    return currentUser.sub !== game.user1_id && !game.user2_id  
  }

  const canReJoin = () => {
    const currentUser = authService.getCurrentUser();
    return currentUser.sub === game.user1_id || currentUser.sub === game.user2_id
  }
  

  useEffect(() => {
    UserService.getUserBoard(game.user1_id).then((res) => {
      setUser1(res.data);
    });
    UserService.getUserBoard(game.user2_id).then((res) => {
      setUser2(res.data);
    });
  }, [game.user1_id, game.user2_id]);

  return (
    <div className="navy-card-container d-flex flex-column align-items-center border border-dark py-4">
      <div className="w-100 d-flex justify-content-center mb-2">
        <img src={wings} alt="Wings" />
      </div>
      <div className="w-75 d-flex justify-content-around align-items-center">
        <NavyUserCard username={user1.username} />
        <p className="navy-text">VS.</p>
        <NavyUserCard username={user2.username} rol={user2.username ? "guest" : "free"}/>
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
