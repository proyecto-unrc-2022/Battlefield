import React, {Component} from "react";

export default class Lobby extends Component{
    render() {
        return (
            <div className="airforce-lobby" style={{textAlign: "center", padding:"15rem 15rem"}}>
                <h1 style={{fontFamily: "Silkscreen"}}>
                Waiting for player...
                </h1>
            </div>
        )
    } 
}