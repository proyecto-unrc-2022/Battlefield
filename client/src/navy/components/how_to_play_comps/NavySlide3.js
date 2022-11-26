import GridShipPlace from "../GridShipPlace"
import "../GridShipPlace.css";


const NavySlide3 = () => {
  const position = {"x": 5, "y":5}

  return (
    <div className="text-break">
      <p className="text-justify">
        Then the ship must be placed, with the initial coordinates and course.
        It should be noted that the ship cannot be initially placed outside the
        grid. Notice that each user places the ship in different halves of the
        board
      </p>
      <div className="row mx-auto mt-3 ">
        <GridShipPlace
          course={"N"}
          cols={20}
          rows={10}
          size={3}
          selectPosition={position}
        />
      </div>
    </div>
  );
};

export default NavySlide3;
