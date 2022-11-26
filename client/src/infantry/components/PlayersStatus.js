import React from "react";
import gameService from "../services/game.service";

export default function PlayersStatus(){

    return(

        <div>
            Hay
        </div>

    )

}


{/*
    export default function PlayersStatus(){

    const [game, setGame] = useState([])
    const [state, setState] = useState([])

    const id_game = localStorage.getItem('id_game')

    const getGame = (id_game) =>{

        gameService.ready(id_game).then(resp =>{
            setGame(resp.data)
        })

    }

    const figure = (game, id_user) =>{

        gameService.character_wait(game.id, id_user).then(resp =>{
            setState(resp)
        })

        if(state === null){
            return false
        }else{
            return true
        }
    }  


}
*/}