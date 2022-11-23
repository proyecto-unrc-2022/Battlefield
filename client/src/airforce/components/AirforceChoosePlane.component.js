import React, { Component} from "react";
import AirforceService from "../services/airforce.service";

import { useParams } from "react-router-dom";

function withParams(Component) {
    return props => <Component {...props} params={useParams()} />;
  }

class ChoosePlane extends Component {

    
    state = {
        id: null,
        course: null,
        coord_x: null,
        coord_y: null,
        ready: false,
        planes: null,
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
    
    id(){
        let { id } = this.props.params;
        return id;
    }

    handleSubmit = (event) => {
        event.preventDefault();
        AirforceService.choosePlaneAndPosition(this.state.id, this.state.course, this.state.coord_x, this.state.coord_y, this.id()).then(
            console.log("player 1 is ready")
        )
    }
    
    planes(){
        AirforceService.getPlanes().then((response) => {
            localStorage.setItem("planes", JSON.stringify(response.data));
        });
    }

    title(key){
        return "Size: " + this.state.planes[key].size + "\nSpeed:" + this.state.planes[key].speed + "\nHealth: " 
        + this.state.planes[key].health + "\nProjectile: " + this.state.planes[key].cant_projecile;
    }
    
        
    render() {          
        // console.log("state " + JSON.parse(localStorage.getItem('planes')).name);
        this.planes();
        this.state.planes = JSON.parse(localStorage.getItem('planes'));
        console.log("planes " + this.state.planes);
        return (
              <div className="container-lobby" style={{textAlign: "center"}}>
                <div className="select-plane">
                    <h2 className="subtitle-1">Choose your plane</h2>
                    <div>
                    {   Object.keys(this.state.planes).map((key) => (
                        <div className="planes-buttons" style={{display: "inline-block", verticalAlign: "middle", padding: "1rem 1rem"}} onClick={() => this.handleClick(key)}>
                            <abbr title= {this.title(key)}>
                                <button className="button-p" >{this.state.planes[key].name}</button>
                            </abbr>
                        </div>
                        ))
                    }
                    </div>
                </div>
                <div>
                    <h2 className="subtitle-2">Choose the position and direction where you want to start</h2>
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
        )
    }
}

export default withParams(ChoosePlane);
