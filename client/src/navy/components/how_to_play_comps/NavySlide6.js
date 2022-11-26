import NavyTitle from "../NavyTitle";

const NavySlide6 = () => {
  return (
    <div className="text-break">
      <NavyTitle text="Some important things to keep in mind." size="medium" />
      <p className="text-justify">
        Inside the game board you can have parts of a ship outside of it, except
        for the bow. Also, the maximum travel distance and forward speed of
        missiles are entirely dependent on the type of ship that is selected at
        the start of the game.
      </p>
      <NavyTitle text="¡Enjoy Navy Battleship!" size="medium" />
    </div>
  );
};

export default NavySlide6;
