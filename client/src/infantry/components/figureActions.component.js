import React, { Component, Alert } from "react";
import InfantryService from "../services/infantry.service"


const EAST = 2
const SOUTH = 0
const SOUTH_EAST = 1
const SOUTH_WEST = 7
const WEST = 6
const NORTH_WEST = 5
const NORTH = 4
const NORTH_EAST = 3

export default class FigureActions extends Component {
//Renderiza todo el panel de control para las acciones del jugador
    constructor(props) {
        super(props);
        this.state = {
        game_id : props.game_id,
        user_id: props.user_id,
        velocity: null
        }  
    }

    async action(direction, action, velocity){
        if(action === "move"){
            let response = await InfantryService.move(this.state.game_id, this.state.user_id,
                direction, velocity)
                if(response === "Accion invalida"){
                    return alert("Movimiento invalido")
                }
            return;
        }
        if(action === "shoot"){
            let response = await InfantryService.shoot(this.state.game_id, this.state.user_id,
                direction)
                if(response === "Accion invalida"){
                    return alert("Movimiento invalido")
                }
                return;
        }
    }
    
    async componentDidMount(){
        let data = await InfantryService.getFigure(this.state.user_id, this.state.game_id)
        if(data["data"]!= null){
            this.setState({
                velocity: data["data"].velocidad
            })
        }
    }
    optionsRender(){
        const options = []
        if(this.state.velocity != null){
            for (let i = 0; i <= this.state.velocity; i++) {
                options.push(<option value={i}>{i}</option>)
            }
        }
        return options
    }
    render(){
        return(
            <div class="container">
                <form onSubmit={ev => {ev.preventDefault();
                this.action(ev.target.direction.value, ev.target.action.value, ev.target.velocity.value)}}>
                    <div class="form-group">
                        <div class="row align-items-start">
                            <input type="radio" class="btn-check" name="direction" id="north west" autocomplete="off" checked value={NORTH_WEST}/>
                                <label class="btn btn-outline-primary col" for="north west">north west</label>
                            <input type="radio" class="btn-check" name="direction" id="north" autocomplete="off" checked value={NORTH}/>
                                <label class="btn btn-outline-primary col" for="north">north</label>
                            <input type="radio" class="btn-check" name="direction" id="north east" autocomplete="off" checked value={NORTH_EAST}/>
                                <label class="btn btn-outline-primary col" for="north east">north east</label>
                        </div>
                        <div class="row align-items-center">
                            <input type="radio" class="btn-check" name="direction" id="west" autocomplete="off" checked value={WEST}/>
                             <label class="btn btn-outline-primary col" for="west">west</label>
                            <div class="col"></div>
                            <input type="radio" class="btn-check" name="direction" id="east" autocomplete="off" checked value={EAST}/>
                                <label class="btn btn-outline-primary col" for="east">east</label>
                        </div>
                        <div class="row align-items-end">
                            <input type="radio" class="btn-check" name="direction" id="south west" autocomplete="off" checked value={SOUTH_WEST}/>
                                <label class="btn btn-outline-primary col" for="south west">south west</label>
                            <input type="radio" class="btn-check" name="direction" id="south" autocomplete="off" checked value={SOUTH}/>
                               <label class="btn btn-outline-primary col " for="south">south</label>
                            <input type="radio" class="btn-check" name="direction" id="south east" autocomplete="off" checked value={SOUTH_EAST}/>
                                <label class="btn btn-outline-primary col" for="south east">south east</label>
                        </div>
                    </div>
                    <div class="form-check">
                        <input class="form-check-input" type="radio" name="action" id="move" value={"move"}/>
                        <label class="form-check-label" for="move">
                            Move
                            <select class="form-select" id="sel1" name="velocity">
                                {this.optionsRender()}
                            </select>
                        </label>
                        
                        <input class="form-check-input" type="radio" name="action" id="shoot" data-toggle="dropdown" value={"shoot"}/>
                        <label class="form-check-label" for="shoot" >
                            Shoot                      
                        </label>
                    </div>
                    <button type="submit" class="btn btn-primary">Submit</button>
                    </form>
            </div>
        ) 
    }
}