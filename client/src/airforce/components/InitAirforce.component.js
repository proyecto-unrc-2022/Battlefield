import { Button } from "bootstrap";
import React, { Component } from "react";
import Form from "react-validation/build/form";
import Input from "react-validation/build/input";

import AirForceService from "../services/airforce.service"

export default class InitAirforce extends Component {
  constructor(props) {
    super(props);

    this.state = {
      content: null,
    };
    }
    inti(){
        AirForceService.createAirforceGame().then(
        () => {
        this.props.router.navigate("/board");
        window.location.reload();
        });
    } 


  render() {
    return (
      <div className="container">
        <header className="jumbotron">
          <h3>AirForceGame</h3>
        </header>
        <button onClick={this.inti}>  
            "sdsadsa"
        </button>

        <Form
            onSubmit={this.inti}
            ref={(c) => {
            this.form = c;
            }}
          >
             <div className="form-group">
                <button
                    className="btn btn-primary btn-block"
                >
                    {this.state.loading && (
                    <span className="spinner-border spinner-border-sm"></span>
                    )}
                    <span>Start Game</span>
                </button>
            </div>
          </Form>
      </div>
    );
  }
}