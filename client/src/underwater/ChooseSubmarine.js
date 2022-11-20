import { useParams } from "react-router-dom";
import AuthService from "../services/auth.service";
import "./css/cards.css"

export default function ChooseSubmarine() {
  const { gameId } = useParams();
  const user = AuthService.getCurrentUser();

  return (
    <div className="u-choose-submarine">
      <h1>Choose your fighter</h1>
      <div className="cards-container">
        <div className="card">
          <img src="https://static-s.aa-cdn.net/img/ios/1451817911/973e1c13fd06634d7de878a801664cc5?v=1" alt="Submarine" />
          <ul>
            <li><strong>Saukko</strong></li>
            <li>Size: 2</li>
            <li>Speed: 5</li>
            <li>visibility: 5</li>
            <li>radar_scope: 8</li>
            <li>health: 10</li>
            <li>torpedo_speed: 5</li>
            <li>torpedo_damage: 5</li>
          </ul>
        </div>
        <div className="card">
          <img src="https://static-s.aa-cdn.net/img/ios/1451817911/973e1c13fd06634d7de878a801664cc5?v=1" alt="Submarine" />
          <ul>
            <li><strong>Saukko</strong></li>
            <li>Size: 2</li>
            <li>Speed: 5</li>
            <li>visibility: 5</li>
            <li>radar_scope: 8</li>
            <li>health: 10</li>
            <li>torpedo_speed: 5</li>
            <li>torpedo_damage: 5</li>
          </ul>
        </div>
        <div className="card">
          <img src="https://static-s.aa-cdn.net/img/ios/1451817911/973e1c13fd06634d7de878a801664cc5?v=1" alt="Submarine" />
          <ul>
            <li><strong>Saukko</strong></li>
            <li>Size: 2</li>
            <li>Speed: 5</li>
            <li>visibility: 5</li>
            <li>radar_scope: 8</li>
            <li>health: 10</li>
            <li>torpedo_speed: 5</li>
            <li>torpedo_damage: 5</li>
          </ul>
        </div>
      </div>
    </div>
  );
}
