import React from 'react'; 
import "./css/board.css"

export default function UnderCell({type, images}){ 
  const rotation = 45 * parseInt([type[type.length-1]]);

  const style = {
    transform: "rotate(" + rotation + "deg)",
  }

  function image() {
    if(/H|T/.test(type)) {
      const typeCode = type.substring(0,2);
      return <img style={style} src={images[typeCode]} width="100%" />
    }
    else return null;
  }

  return (<div className={"u-cell u-cell-" + type} >{image()}</div>)
}
