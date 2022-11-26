import React, { Component } from "react";
import Guerra from '../images/Guerra.png'

export default class Imagenes extends Component {

render(){

    return <div class="container">
        <div class="row">
            <div class="col">
                <img src= {Guerra} class="rounded float-start"/>
            </div>
        </div>
    </div>

}
}


