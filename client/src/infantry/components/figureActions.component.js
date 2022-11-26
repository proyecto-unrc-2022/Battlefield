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
            game_id: props.game_id,
            user_id: props.user_id,
            velocity: null
        }
    }

    async action(direction, action, velocity) {
        if (action === "move") {
            let response = await InfantryService.move(this.state.game_id, this.state.user_id,
                direction, velocity)
            if (response === "Accion invalida") {
                return alert("Movimiento invalido")
            }
            return;
        }
        if (action === "shoot") {
            let response = await InfantryService.shoot(this.state.game_id, this.state.user_id,
                direction)
            if (response === "Accion invalida") {
                return alert("Movimiento invalido")
            }
            return;
        }
    }

    async componentDidMount() {
        let data = await InfantryService.getFigure(this.state.user_id, this.state.game_id)
        if (data["data"] != null) {
            this.setState({
                velocity: data["data"].velocidad
            })
        }
    }
    optionsRender() {
        const options = []
        if (this.state.velocity != null) {
            for (let i = 0; i <= this.state.velocity; i++) {
                options.push(<option value={i}>{i}</option>)
            }
        }
        return options
    }
    render() {
        return (
            <div class="container">
                <form onSubmit={ev => {
                    ev.preventDefault();
                    this.action(ev.target.direction.value, ev.target.action.value, ev.target.velocity.value)
                }}>
                    <div class="form-group">
                        <div class="row align-items-start">
                            <div>
                                <input type="radio" class="btn-check col" name="direction" id="north west" autocomplete="off" checked value={NORTH_WEST} />
                                <label class="btn btn-secondary col" for="north west">North west</label>

                            </div>
                            <div>
                                <input type="radio" class="btn-check col" name="direction" id="north" autocomplete="off" checked value={NORTH} />
                                <label class="btn btn-secondary col" for="north">North</label>
                            </div>
                            <div>
                                <input type="radio" class="btn-check col" name="direction" id="north east" autocomplete="off" checked value={NORTH_EAST} />
                                <label class="btn btn-secondary col" for="north east">North east</label>
                            </div>
                        </div>

                        <div class="row align-items-center">
                            <div class="position-absolute top-50 start-50 translate-middle">
                                <input type="radio" class="btn-check" name="direction" id="west" autocomplete="off" checked value={WEST} />
                                <label class="btn btn-secondary" for="west">West</label>
                            </div>
                            <div class="col"></div>
                            <div class="col-7">
                                <div class="col aling-self-start">
                                    <input type="radio" class="btn-check col-md-4 aling-self-end" name="direction" id="east" autocomplete="off" checked value={EAST} />
                                </div>
                                <label class="btn btn-secondary col-3" for="east">East</label>
                            </div>
                        </div>

                        <div class="row align-items-end">
                            <div>
                                <label class="btn btn-secondary col" for="south west">South west</label>
                                <input type="radio" class="btn-check col" name="direction" id="south west" autocomplete="off" checked value={SOUTH_WEST} />
                            </div>
                            <div>
                                <label class="btn btn-secondary col " for="south">South</label>
                                <input type="radio" class="btn-check col" name="direction" id="south" autocomplete="off" checked value={SOUTH} />
                            </div>
                            <div>
                                <label class="btn btn-secondary col" for="south east">South east</label>
                                <input type="radio" class="btn-check col" name="direction" id="south east" autocomplete="off" checked value={SOUTH_EAST} />
                            </div>
                        </div>
                    </div>
                    <div class="form-check">
                        <input class="form-check-input" type="radio" name="action" id="move" value={"move"} />
                        <label class="form-check-label text-white" for="move">
                            Move
                            <select class="form-select" id="sel1" name="velocity">
                                {this.optionsRender()}
                            </select>
                        </label>
                        <input class="form-check-input" type="radio" name="action" id="shoot" value={"shoot"} />
                        <label class="form-check-label text-white" for="shoot">
                            Shoot
                        </label>
                    </div>
                    <button type="submit" class="btn btn-secondary">Enter</button>
                </form>
            </div>
        )
    }
}