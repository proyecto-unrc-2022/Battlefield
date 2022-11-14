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
        this.updateData()
    }
    updateData(){
        let data = InfantryService.getInfantry(this.state.user_id, this.state.game_id)
        data.then((datos) => this.setState({
            pos_x: datos.pos_x,
            pos_y: datos.pos_y,
            hp: datos.hp,
            tamaño: datos.tamaño,
            velocidad: datos.velocidad,
            direccion: datos.direccion,
            avail_actions: datos.avail_actions
        }))

    }
    render(){
        return <div>
            <h3>Jugador {this.state.user_id}</h3>
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