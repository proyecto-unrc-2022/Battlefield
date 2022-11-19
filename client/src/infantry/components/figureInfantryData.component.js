import React, { Component } from "react";
import InfantryService from "../services/infantry.service"
export default class FigureInfantryData extends Component {
    constructor(props) {
        super(props);
        this.state = {
            game_id: props.game_id,
            user_id: props.user_id,
            pos_x: null,
            pos_y: null,
            hp: null,
            tamaño: null,
            velocidad: null,
            direccion: null,
            avail_actions: null
        }
        
    }
    updateData(){
        let data = InfantryService.getFigure(this.state.user_id, this.state.game_id)
        data.then((datos) => this.setState({
            pos_x: datos["data"].pos_x,
            pos_y: datos["data"].pos_y,
            hp: datos["data"].hp,
            tamaño: datos["data"].tamaño,
            velocidad: datos["data"].velocidad,
            direccion: datos["data"].direccion,
            avail_actions: datos["data"].avail_actions
        }))

    }
    render(){
        this.updateData()
        return <div>
            <h3>Player {this.state.user_id}</h3>
            <ul>
                <li>
                    HP: {this.state.hp}
                </li>
                <li>
                    x : {this.state.pos_x}
                </li>
                <li>
                    y : {this.state.pos_y}
                </li>
                <li>
                    acciones disponibles : {this.state.avail_actions}
                </li>
            </ul>
        </div>
    }
}