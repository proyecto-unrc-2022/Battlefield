import React, { useState } from "react";

export default function UnderNewGame({setVisibleComp}) {
  const [rangevalH, setRangevalH] = useState(10);  
  const [rangevalW, setRangevalW] = useState(20); 

  return (
    <form>
      <div className="u-small-container">
        <div className="row">
          <div className="u-input-field">
            <label for="height">Height</label>
            <input type={"range"} min="10" max="20" step="2" id="height" value={rangevalH} onChange={(event) => setRangevalH(event.target.value)}/>
            <span style={{margin: "12px"}}>{rangevalH}</span>

            <label for="width">Width</label>
            <input type={"range"} min="20" max="40" step="2" id="width" value={rangevalW} onChange={(event) => setRangevalW(event.target.value)}/>
            <span style={{margin: "12px"}}>{rangevalW}</span>
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
          <div onClick={() => {setVisibleComp("home")}} className="u-button">‹</div>
          <button id="play-button" className="u-button">Play</button>
        </div>
      </div>
    </form>
  );
}