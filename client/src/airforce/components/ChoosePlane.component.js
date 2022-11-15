import React, { Component} from "react";
import { useParams } from "react-router-dom";

function withParams(Component) {
    return props => <Component {...props} params={useParams()} />;
}

class ChoosePlane extends Component {
    id(){
        let { id } = this.props.params;
        return id;
    }
    render() {return (
        <div className="container-lobby" style={{textAlign: "center"}}>
            <h1 style={{fontFamily: "Silkscreen"}}>Lobby ID = {this.id()}</h1>
        </div>
    )}
}
export default withParams(ChoosePlane);

