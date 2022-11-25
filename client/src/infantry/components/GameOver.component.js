import React, { Component } from "react";
import InfantryService from "../services/infantry.service";

export default class GameOverClass extends Component {
  constructor(props) {
    super(props);
    this.state = {
      game_id: props.game_id,
      player1_id: props.player1_id,
      player2_id: props.player2_id,
      figure1: null,
      figure2: null,
    }
  }

  async componentDidMount() {
    const f1 = await InfantryService.getFigure(this.state.player1_id, this.state.game_id)
    const f2 = await InfantryService.getFigure(this.state.player2_id, this.state.game_id)
    this.setState({
      figure1: f1["body"],
      figure2: f2["body"],
    })
  }

  GameOver() {

    if (this.state.figure1 != null || this.state.figure2 != null) {
      console.log(this.state.figure1)
      if (this.state.figure1.hp <= 0 || this.state.figure2.hp <= 0) {
        return <div>
          Game Over
        </div>
      }
    }
  }

  render() {

    return <div> {this.GameOver(this.state.figure1, this.state.figure2)}  </div>

  }
}
