import React from 'react'; 
import "./css/game-style.css"
import { GoPrimitiveDot } from "react-icons/go";

export default function UnderCell({placeSubmarine, x, y, type, images}){ 
  const rotation = 45 * parseInt([type[type.length-1]]);

  const style = {
    transform: "rotate(" + rotation + "deg)",
  }

  function image() {
    if(/H|T/.test(type)) {
      const typeCode = type.substring(0,2);
      return <img style={style} src={images[typeCode]} width="100%" />
    }
    if(/rP/.test(type))
      return <GoPrimitiveDot style={{color: "cyan"}} />
    else return null;
  }

  return (<div onClick={placeSubmarine == null ? null : _ => placeSubmarine(x,y)} className={"u-cell u-cell-" + type} >{image()}</div>)
}