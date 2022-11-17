import React from 'react';
import { GiSandsOfTime } from "react-icons/gi";
import "./css/style.css"

export default function UnderLoading() {
    // const [rotate, setRotate] = React.useState(false);
    // timing(){
    //     setInterval(() => {
    //       setRotate(!rotate);
    //     }, 1000);
    //     console.log(rotate);
    // }
    return (
        <div className='u-container'>
            <div className='u-titlecenter'>Waiting for players...</div>
            <GiSandsOfTime size='40px' />
        </div>
    );
}

