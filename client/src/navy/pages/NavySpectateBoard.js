import React, { useEffect,useState } from 'react'
import { useParams} from 'react-router-dom'
import NavySpectateGameService from '../services/NavySpectateGameService'
import NavyGameService from '../services/NavyGameService'
import NavyShipCard from '../components/NavyShipCard'

const NavySpectateBoard = () => {
  const {id} = useParams();
  const [spectateInfo, setSpectateInfo] = useState({});
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    NavyGameService.getNavyGame(id).then((res) => {
      const round = res.data.data.round;
      NavySpectateGameService.getNavySpectateGames(id,round-2).then((res) => {
        console.log(res.data.data); 
        setSpectateInfo(res.data.data);
        setLoading(false);
      });
    });    
      
  }, []);

  return (
    <>
      {!loading ? (
      <div>
      <h1>Spectate Board</h1>
      <h2>Player 1: {spectateInfo.game.user_1.username}</h2>
      <h2>Round: {spectateInfo.game.round}</h2>
      <h2>Player 2: {spectateInfo.game.user_2.username}</h2>
      <h2>Winner: { spectateInfo.game.winner ? spectateInfo.game.winner.username : "No winner yet"}</h2>
      <div className="row d-flex flex justify-content-center" style={{gap: "120px"}}>
      {spectateInfo.ships.map((ship) => (
        <NavyShipCard ship={ship} name={ship.name} />

        ))}
        </div>

          {spectateInfo.ships.map((ship) => (
              <ul>
                <li>SHIP USER: {ship.user_id}</li>
                <li>Ship name: {ship.name}</li>
                <li>Ship size: {ship.size}</li>
                <li>Ship pos_x: {ship.pos_x}</li>
                <li>Ship pos_y: {ship.pos_y}</li>
                <li>Ship course: {ship.course}</li>
                </ul>
          ))}
      </div>
      )
       : (
        <h1>Loading...</h1>
      )}
    <div>NavySpectateBoard</div>
    </>
  )
}

export default NavySpectateBoard