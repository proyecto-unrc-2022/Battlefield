import AirforceBoard from "./AirforceBoard.component";
import React, { Component } from "react";

export default class GameRoom extends Component{
    render(){
        return(
            <div>
             {<AirforceBoard />}
            </div>
        )
    }
}
