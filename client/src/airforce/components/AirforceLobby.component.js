import { Button } from "bootstrap";
import React, { Component, useState} from "react";
import AirforceService from "../services/airforce.service";

import { useParams } from "react-router-dom";

function withParams(Component) {
    return props => <Component {...props} params={useParams()} />;
  }

class AirforceLobby extends Component {
    
    state = {
        id: null,
        course: null,
        coord_x: null,
        coord_y: null,
        ready: false,
    }
    
    
    handleChangeCourse = (event) => {
        const {value} = event.target
        this.setState({
            course: value
        })
        console.log(this.state.course)
        
    }
    
    handleChangeCx = (event) => {
        const {value} = event.target
        this.setState({
            coord_x: value
        })
        console.log(this.state.coord_x)
        
    }
    
    handleChangeCy = (event) => {
        const {value} = event.target
        this.setState({
            coord_y: value
        })
        console.log(this.state.coord_y)
        
    }
    
    handleClick(idPlane){
        this.setState({
            id: idPlane
        })
        console.log(this.state.id)
    }
    
    handleSubmit = () => {
        AirforceService.choosePlaneAndPosition(this.state.id, this.state.course, this.state.coord_x, this.state.coord_y).then(
            console.log("player 1 is ready")
        )
    }
    
    
    redirect = (id) => {
        window.location.href = "/airforce/game/"+id+"/choose/plane"
    }
    
    id(){
        let { id } = this.props.params;
        return id;
    }
        
    render() {
        console.log(this.id());
        setInterval(() => {
            AirforceService.airforceGameReady(this.id()).then((response) => {
                this.state.ready =  response.data.ready;
            }
            );
            if(this.state.ready){
                this.redirect(this.id());
            }
          }, 2000 ); 
            return (
              <div className="container-lobby" style={{textAlign: "center"}}>
                <h1 style={{fontFamily: "Silkscreen"}}>Lobby ID = {this.id()}</h1>
                <div className="select-plane">
                    <h4 className="subtitle-1">Choose your plane</h4>
                    <div className="planes-buttons" style={{display: "inline-block", verticalAlign: "middle", padding: "1rem 1rem"}} onClick={() => this.handleClick(1)}>
                        <button className="button-p" >Hawker Tempest</button>
                    </div>
                    <div className="planes-buttons"  style={{display: "inline-block", verticalAlign: "middle", padding: "1rem 1rem"}} onClick={() => this.handleClick(2)}>
                        <button className="button-p" >Mitsubishi A6M Zero</button>
                    </div>
                    <div className="planes-buttons"  style={{display: "inline-block", verticalAlign: "middle", padding: "1rem 1rem"}} onClick={() => this.handleClick(3)}>
                        <button className="button-p" >Douglas A-20 Havoc</button>
                    </div>
                    <div className="planes-buttons"  style={{display: "inline-block", verticalAlign: "middle", padding: "1rem 1rem"}} onClick={() => this.handleClick(4)}>
                        <button className="button-p" >Boeing B-17 Flying Fortress</button>
                    </div>
                    <div>
                        <h4 className="subtitle-2">Choose the position and direction where you want to start</h4>
                        <form>
                            <abbr title="1- North 2- East 3- South 4- West">
                            <input className="input-bar" required type="text" placeholder="Course (1-4)"  onChange={this.handleChangeCourse}/>
                            </abbr>
                            <input className="input-bar" required type="text" placeholder="Coordinate X (1-20)" onChange={this.handleChangeCx}/>
                            <input className="input-bar" required type="text" placeholder="Coordinate Y (1-10)" onChange={this.handleChangeCy}/>
                            <button  type="submit" className="ready-button" style={{marginTop: 50}} onClick={this.handleSubmit}>
                                Ready!! 
                            </button>
                        </form>
                    </div>
                </div>
            </div>
        )
    }
}

export default withParams(AirforceLobby);
