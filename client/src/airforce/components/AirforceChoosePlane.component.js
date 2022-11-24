import React, { Component} from "react";
import { Routes, Route, useParams, useNavigate} from "react-router-dom";
import AirforceService from "../services/airforce.service";
import GameRoom from "./AirforceGameRoom.component"
import "./AirforceChoosePlane.css"

function withParams(Component) {
    return props => <Component {...props} param={useParams()}/>;
  }

class ChoosePlane extends Component {
 
    
    state = {
        id: null,
        course: null,
        coord_x: null,
        coord_y: null,
        ready: false,
        planes: null,
        ready: false,
    }

    

    
    handleChangeCourse = (event) => {
        const {value} = event.target
        this.setState({
            course: value
        })
        
    }
    
    handleChangeCx = (event) => {
        const {value} = event.target
        this.setState({
            coord_x: value
        })
        
    }
    
    handleChangeCy = (event) => {
        const {value} = event.target
        this.setState({
            coord_y: value
        })
        
    }
    
    handleClick(idPlane){
        this.setState({
            id: idPlane
        })
    }
    
    id(){
        let { id } = this.props.param;
        return id;
    }


    handleSubmit = (event) => {
        event.preventDefault();
        console.log(JSON.parse(localStorage.getItem("user")))
        AirforceService.choosePlaneAndPosition(this.state.id, this.state.course, this.state.coord_x, this.state.coord_y, this.id()).then(
            (response) => {
                if (response.status === 200) 
                localStorage.setItem("id", this.id())
                localStorage.setItem("coord_x", this.state.coord_x)
                localStorage.setItem("coord_y", this.state.coord_y)
                localStorage.setItem("course", this.state.course)
                window.location.href = "/airforce/game/"+this.id()+"/room"
                

            }
        )
    }
    
    planes(){
        AirforceService.getPlanes().then((response) => {
            console.log( JSON.stringify(response.data))
            localStorage.setItem("planes", JSON.stringify(response.data));
        });
    }

    title(key){
        return "Size: " + this.state.planes[key].size + "\nSpeed:" + this.state.planes[key].speed + "\nHealth: " 
        + this.state.planes[key].health + "\nProjectile: " + this.state.planes[key].cant_projecile;
    }

    redirect = (id) => {
        window.location.href = "/airforce/game/"+id+"/gameRoom"
    }
    
        
    render() {        
        
        setInterval(() => {
            AirforceService.airforceChoosePlaneReady(this.id()).then((response) => {
                this.state.ready =  response.data.status;
            }
            );
            console.log("ssss" + this.state.ready);
            if(this.state.ready){
                this.redirect(this.id());
            }
          }, 20000 ); 

        // console.log("state " + JSON.parse(localStorage.getItem('planes')).name);
        this.planes();
        this.state.planes = JSON.parse(localStorage.getItem('planes'));
        return (
              <div className="container-choosePlane" style={{textAlign: "center"}}>
               <link href='https://fonts.googleapis.com/css?family=Silkscreen' rel='stylesheet'></link>
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
