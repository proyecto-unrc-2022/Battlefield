import SlideActionCard from "./SlideActionCard";
import React, { useEffect, useState } from "react";


const NavySlide5 = () => {
  const [move, setMove] = useState(false);
  const [myShip, setMyShip] = useState(null);
  const [action, setAction] = useState({
    course: " ",
    move: 0,
    attack: 0,
  });


  const handleNewCourse = (newCourse) => {
    setAction({ ...action, course: newCourse });
  };

  const handleAttack = () => {
    setAction({ ...action, attack: 1, move: 0 });
    setMove(false);
  };

  const handleMove = (quant) => {
    setMove(true);
    setAction({ ...action, attack: 0, move: quant });
  };


  return (
    <div className="text-break">
      <p className="text-justify ">
        Finally, to send an action, a menu will be available. The menu will
        allow us to perform two types of actions: Turn and shoot, or Turn and
        move. Please note that in order to see game updates, we need to click on
        the "Refresh" option once both players have submitted their action.
      </p>

      <div className="row justify-content-center mt-5">
        <div className="col-10">
          <SlideActionCard
            ship={myShip}
            changeCourse={handleNewCourse}
            changeAttack={handleAttack}
            changeMove={handleMove}
            attack={action.attack === 0 ? false : true}
            move={move}
          />
        </div>
      </div>
    </div>
  );
};

export default NavySlide5;
