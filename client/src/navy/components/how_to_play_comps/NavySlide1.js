import "./NavySlider.css";
import NavyTitle from "../NavyTitle";

const NavySlide1 = () => {
  return (
    <div className="text-break">
      <NavyTitle text="¡Welcome to Navy Battleship!" size="medium" />
      <p className="text-justify">
        Dynamic Navy Battleship is an interactive, turn-based game for two
        players. It takes place in a common navigable space arranged in the form
        of a grid, with a size of 20 squares long by 10 squares high. Each
        player chooses a ship to play with, there are 4 possible ships, which
        differ in their characteristics: ship size, ship speed, health/energy,
        missile speed, and missile damage.
      </p>
    </div>
  );
};

export default NavySlide1;
