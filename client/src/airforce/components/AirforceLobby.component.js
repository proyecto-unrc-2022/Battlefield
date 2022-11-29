import React, { Component, useState} from "react";
import AirforceService from "../services/airforce.service";
import "./AirforceLobby.css"

import { useParams, useHistory } from "react-router-dom";




function withParams(Component) {
    return props => <Component {...props} params={useParams()} />;
  }


class AirforceLobby extends Component {    



    state = {
        ready: false,
    }
    
    redirect = (id) => {
        window.location.href = "/airforce/game/"+id+"/choose/plane"
    }
    
    id(){
        let { id } = this.props.params;
        return id;
    }
        
    render() {
        setInterval(() => {
                AirforceService.airforceGameReady(this.id()).then((response) => {
                    this.state.ready =  response.data.status;
                });
            if(this.state.ready){
                this.redirect(this.id());
            }
          }, 2000 ); 
            return (               
            <div className="airforce-lobby" style={{textAlign: "center", padding:"15rem 15rem"}}>
                <h1 style={{fontFamily: "Silkscreen"}}>Lobby ID = {this.id()}</h1>
                <h1 style={{fontFamily: "Silkscreen"}}>
                    Waiting for player...
                </h1>
            </div>

        )
    }
}

export default withParams(AirforceLobby);