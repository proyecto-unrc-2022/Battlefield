import React, { Component } from "react";
import AuthService from "../../services/auth.service";

/**
 * Muestra informacion del jugador, como la id, la vida y coordenadas de donde se encuentra
 */
export default class FigureInfantryData extends Component {
    constructor(props) {
        super(props);
        this.state = {
            figure: props.figure
        }
    }
    render(){
        let user
        if(this.state.figure.id_user === AuthService.getCurrentUser().sub){
            user = "You"
        }else{
            user = "Opponent"
        }
        return <div>
        <div class="text-center h4 pb-2 mb-4 text-black border-bottom border-strong-black">
            <h3>{user}</h3>
        </div>
        <table class="table table-dark table-striped" >
        <tbody class="headt">
            <tr class = "text-center">
                <th scope="row">HP</th>
                <td>{this.state.figure["hp"]}</td>
            </tr>
            <tr class = "text-center">
                <th scope="row">x</th>
                <td>{this.state.figure["pos_x"]}</td>
            </tr>
            <tr class = "text-center">
                <th scope="row">y</th>
                <td colspan="2">{this.state.figure["pos_y"]}</td>
            </tr>
        </tbody>
    </table>
    </div >
    }
}