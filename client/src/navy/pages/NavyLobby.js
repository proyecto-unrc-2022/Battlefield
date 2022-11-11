import React, { useEffect, useState } from "react";
import { useParams } from "react-router-dom";
import NavyGameService from "../services/NavyGameService";


const NavyLobby = () => {
  const id = useParams();
  const [game, setGame] = useState({});

  console.log(id)
  useEffect(() => {
    NavyGameService.getNavyGame(id).then((resp) => {
      console.log(resp.data.data);
      setGame(resp.data.data);
    });
  }, []);
  console.log(game)

  return <div>NavyLobby</div>;
};

export default NavyLobby;
