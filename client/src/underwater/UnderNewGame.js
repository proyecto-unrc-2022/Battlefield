import React, { useState } from "react";
import axios from "axios";

const baseURL = "http://127.0.0.1:5000/api/v1/underwater";

export default function UnderNewGame(props) {
  const [height, setHeight] = useState(10);  
  const [width, setWidth] = useState(20); 
  const [post, setPost] = useState(null);

  function onSubmit(e) {
    e.preventDefault();

    axios.post(
      baseURL + "/game/new",
      {},
      {
        headers: { 'Authorization': `Bearer ${props.token}` }
      }
    ).then((response) => {setPost(response.data);});
    console.log(post);
  }

  return (
      <div className="u-small-container">
        <form onSubmit={onSubmit}>
        <div className="row">
          <div className="u-input-field">
            <label for="height">Height</label>
            <input type={"range"} min="10" max="20" step="2" id="height" value={height} onChange={(event) => setHeight(event.target.value)}/>
            <span style={{margin: "12px"}}>{height}</span>

            <label for="width">Width</label>
            <input type={"range"} min="20" max="40" step="2" id="width" value={width} onChange={(event) => setWidth(event.target.value)}/>
            <span style={{margin: "12px"}}>{width}</span>
          </div>

          <div className="u-input-field">
            <label className="inline-block" for="players">Players</label>
            <select type="select" id="players">
              <option value="2">2</option>
              <option value="4">4</option>
            </select>
          </div>
        </div>

        <div className="row u-input-field">
          <div onClick={() => {props.setVisibleComp("home")}} className="u-button">‹</div>
          <button id="play-button" className="u-button">Play</button>
        </div>
      </form>
    </div>
  );
}
