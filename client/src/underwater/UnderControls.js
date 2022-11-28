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
          <button className="u-game-button"> <CiLocationArrow1 size={40} style = {{transform: 'rotate(-45deg)' }}/></button>
          <input style={{width: "3em"}} type="number" min="0" value={steps} onChange={event => {setSteps(event.target.value)}}></input>
        </div>
      </form>
    );
  }
  
  function ActionButtons() {
    const style = {
      display: "flex",
      alignItems: "center",
      gap: "20px"
    }

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
    
    return (
      <div style={style}>
        <button className="u-game-button" onClick={skip}>Skip</button>
        <button className="u-game-button" onClick={useRadar}>Radar</button>
        <button className="u-game-button" onClick={attack}><GiTorpedo style={{verticalAlign: "bottom"}} size={40} /></button>
      </div>
    );
  }

  useEffect(_ => {setAlertMessage(null)},[props.visibleState]);
  
  return (
    <div style={{display: 'flex', flexDirection: 'column', width: '97%'}}>
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
