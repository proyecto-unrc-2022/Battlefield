import { Button } from "bootstrap";
import React, { Component } from "react";



export default class AirforceLobby extends Component {

    render () {
        return (
            <div>
                <h1 style={{textAlign:"center"}}>Welcome to the lobby</h1>
                <header style={{textAlign:"center"}}> 
                        Waiting for player...
                </header>
            </div>
        )
    }
}
