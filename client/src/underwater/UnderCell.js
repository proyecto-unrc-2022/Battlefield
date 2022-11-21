import React from 'react'; 
import "./css/board.css"

export default function UnderCell({type}){ 
    function selectSymbol() {
        if(/H/.test(type))
            return "∩";
        if(/T/.test(type))
            return "||";
        if(/\*/.test(type))
            return "*";
        else return null;
    }

    const rotation = 45 * parseInt([type[type.length-1]]);

    const style = {
        transform: "rotate(" + rotation + "deg)",
    }

    return (<div className={"u-cell u-cell-" + type} ><span style={style}>{selectSymbol()}</span></div>)
}