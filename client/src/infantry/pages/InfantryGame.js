import React, { useEffect, useState } from "react";
import GameInfantry from "../components/gameInfantry.component";
import infantryService from "../services/infantry.service";

export default function InitGameInfantry(){


    return(
        <div>
            <GameInfantry game_id={1}>

            </GameInfantry>
        </div>
    )
}