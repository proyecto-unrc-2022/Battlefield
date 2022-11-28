import React, { useEffect, useState } from "react";
import { useParams } from "react-router-dom";
import axios from "axios";
import AuthService from "../services/auth.service"
import { CiLocationArrow1} from "react-icons/ci";
import { GiTorpedo } from "react-icons/gi" ;
import authHeader from "../services/auth-header";
export default function UnderControls(props) {

  const [alertMessage, setAlertMessage] = useState(null);
  const params = useParams();
  const sessionId = params["id"];
  const gameURL = "http://localhost:5000/api/v1/underwater/game/" + sessionId;

  function DirectionControl(props) {
    const rotation = 45 * props.position.direction;

    const style = {
      transform: "rotate(" + rotation + "deg)",
    }

    function setDirection(dir) {
      props.setPosition({ x: props.position.x, y: props.position.y, direction: dir });
    }

    const array1 = [7, 0, 1, 6];
    const array2 = [2, 5, 4, 3];

    return (
      <div style={{ position: 'relative', height: 157, width: 157 }}>
        <img style={style} className="u-overlap-1" src={require('./css/images/direc.png')} width="100%" />
        <div className="u-overlap-2 u-direction-grid">
          {array1.map(i => { return (<div key={i} style={{ height: "100%", width: "100%" }} onClick={_ => setDirection(i)}></div>) })}
          <div style={{ height: '100%', width: '100%' }}></div>
          {array2.map(i => { return (<div key={i} style={{ height: "100%", width: "100%" }} onClick={_ => setDirection(i)}></div>) })}
        </div>
      </div>
    );
  }

  function AdvanceControl() {
    const [steps, setSteps] = useState(0);

    function advance(event) { 
      event.preventDefault();

      let headers = authHeader();
      headers["Content-Type"] = "application/json";
      axios.post(
        gameURL + "/rotate_and_advance",
        {
          "direction": props.position.direction,
          "steps": parseInt(steps)
        },
        {headers: headers}
      ).then(_ => console.log("Submarine advance")
      ).catch(error => {
        console.log(error.response.data);
        setAlertMessage(error.response.data["error"]);
      });
    }

    const style = {
      display: "flex",
      gap: "20px",
      alignItems: "center"
    }
    
    return (
      <form onSubmit={advance}> 
        <div style={style}>
          <button className="u-control-button" title="advance"><img src={require("./css/buttons/advancebutton.png")} width="60" height="60"/></button>
          <input className="u-number-input" type="number" min="0" value={steps} onChange={event => {setSteps(event.target.value)}}></input>
        </div>
      </form>
    );
  }
  
  function ActionButtons() {
    function skip() { // Implemented as advancing 0 steps
      let headers = authHeader();
      headers["Content-Type"] = "application/json";
      axios.post(
        gameURL + "/rotate_and_advance",
        {
          "direction": props.visibleState.submarine.direction,
          "steps": 0
        },
        {headers: headers}
      ).then(_ => console.log("Skipped this turn")
      ).catch(error => {
        console.log(error.response.data);
        setAlertMessage(error.response.data["error"]);
      });
    }

    function useRadar() {
      axios.post(
        gameURL + "/send_radar_pulse",
        {},
        {headers: authHeader()}
      ).then(_ => console.log("Radar pulse command sent")
      ).catch(error => {
        console.log(error.response.data);
        setAlertMessage(error.response.data["error"]);
      });
    }

    function attack() {
      let headers = authHeader();
      headers["Content-Type"] = "application/json";
      axios.post(
        gameURL + "/rotate_and_attack",
        {"direction": props.position.direction},
        {headers: headers}
      ).then(_ => {
        console.log("Attack command sent");
      }).catch(error => {
        console.log(error.response.data);
        setAlertMessage(error.response.data["error"]);
      });
    }
    
    const style = {
      display: "flex",
      flexDirection: "row",
      justifyContent: "center",
      alignItems: "center",
      gap: "10px"
    }

    return (
      <div style={style}>
        <button className="u-control-button" onClick={skip} title="skip"><img src={require("./css/buttons/skipbutton.png")} width="60" height="60"/></button>
        <button className="u-control-button" onClick={useRadar} title="radar pulse"><img src={require("./css/buttons/radarbutton.png")} width="60" height="60"/></button>
        <button className="u-control-button" onClick={attack} title="attack"><img src={require("./css/buttons/missilebutton.png")} width="60" height="60"/></button>
      </div>
    );
  }

  useEffect(_ => {setAlertMessage(null)},[props.visibleState]);
  
  return (
    <div style={{display: 'flex', flexDirection: 'column', width: '100%'}}>
      <div className="u-controls-container">
        <div className="u-left-controls">
          <DirectionControl position={props.position} setPosition={props.setPosition} />
          <AdvanceControl />
        </div>
        <div className="u-right-controls">
          <ActionButtons />
        </div>
      </div>
      <div>
        {alertMessage != null ? <p className="u-alert-danger">{alertMessage}</p> : null}
      </div>
    </div>
  );
}
