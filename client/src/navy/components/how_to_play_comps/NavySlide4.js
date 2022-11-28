import board from "../../assets/board.png"

const NavySlide4 = () => {
  return (
    <div className="text-break">
      <p className="text-justify">
        Once the ship is placed, we will see the game board along with other
        options. On the board we will have a sight range where we will see the
        information of the enemy when it appears in that range.
      </p>
      <img src={board} alt="Board"></img>
    </div>
  );
};

export default NavySlide4;
