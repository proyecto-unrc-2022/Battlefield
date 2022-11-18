import {Link} from "react-router-dom";
import "./css/style.css"

export default function UnderHome() {
  return (
    <div className="u-options">
      <Link to="new" className="u-big-button">New Game</Link>
      <Link to="lobby" className="u-big-button">Join Game</Link>
    </div>
  );
}
