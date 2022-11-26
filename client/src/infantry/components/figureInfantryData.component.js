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
    updateData() {
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
    render() {
        this.updateData()
        return <div>
            <div class="text-center h4 pb-2 mb-4 text-black border-bottom border-strong-black">
                <h3>Player {this.state.user_id}</h3>
            </div>
            <table class="table table-dark table-striped">
            <tbody>
                <tr>
                    <th scope="row">HP:</th>
                    <td>{this.state.hp}</td>
                </tr>
                <tr>
                    <th scope="row">x:</th>
                    <td>{this.state.pos_x}</td>
                </tr>
                <tr>
                    <th scope="row">y:</th>
                    <td colspan="2">{this.state.pos_y}</td>
                </tr>
                <tr>
                    <th scope="row">Acciones Disponibles:</th>
                    <td colspan="2">{this.state.avail_actions}</td>

                </tr>
            </tbody>
        </table>
        </div >
    }
}