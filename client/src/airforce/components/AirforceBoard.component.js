 import React, { Component, useRef, useEffect} from "react";
import airforceService from "../services/airforce.service";
import "./AirforceBoard.css"


export default function AirforceBoard(json, r){
    var x = 1;
    var y = 2;
    var cell;
    var round = r;
    useEffect(() => {

        for (let i = 1; i <= 10; i++) {
            for (let j = 1; j <= 20; j++) {
                x = j;
                y = i;
                cell = document.getElementById(`(${x},${y})`)
                cell.innerHTML = "";
            }
        }
        round = r;
        json = JSON.parse(json);    
            Object.keys(json).forEach(key => {
                console.log(key, json[key]);
                x = json[key].x;
                y = json[key].y;
                cell = document.getElementById(`(${x},${y})`)
                if(cell != null) {
                     if(json[key].flying_obj_class == "Plane"){
                         switch (json[key].course){
                             case 1:
                                 cell.innerHTML = "↟";
                               break;
                             case 2:
                                 cell.innerHTML = "↠";
                                 break;
                             case 3:
                                 cell.innerHTML = "↡"
                                 break;
                             case 4:
                                 cell.innerHTML = "↞";
                                 break;
                         }
                    }else{
                        cell.innerHTML = "*";
                    }
                }   
            });   
    }, []);
    

    // cell = document.getElementById(`(${json.planes.p1.x},${json.planes.p1.y})`)
    // cell.innerHTML = "X";
    // cell = document.getElementById(`(${json.planes.p2.x},${json.planes.p2.y})`)
    // cell.innerHTML = "Y";
    return(
        <div className="board">
            <div>Round {round}</div>
                <table>
                <tbody>
                    <tr>   
                         <th></th>
                        <th>0</th>
                        <th>1</th>
                        <th>2</th>
                        <th>3</th>
                        <th>4</th>
                        <th>5</th>
                        <th>6</th>
                        <th>7</th>
                        <th>8</th>
                        <th>9</th>
                        <th>10</th>
                        <th>11</th>
                        <th>12</th>
                        <th>13</th>
                        <th>14</th>
                        <th>15</th>
                        <th>16</th>
                        <th>17</th>
                        <th>18</th>
                        <th>19</th>
                        <th>20</th>
                    </tr>
                    <tr>
                        <th>10</th>
                            <td><div id="(0,10)"></div></td>
                            <td><div id="(1,10)"></div></td>
                            <td><div id="(2,10)"></div></td>
                            <td><div id="(3,10)"></div></td>
                            <td><div id="(4,10)"></div></td>
                            <td><div id="(5,10)"></div></td>
                            <td><div id="(6,10)"></div></td>
                            <td><div id="(7,10)"></div></td>
                            <td><div id="(8,10)"></div></td>
                            <td><div id="(9,10)"></div></td>
                            <td><div id="(10,10)"></div></td>
                            <td><div id="(11,10)"></div></td>
                            <td><div id="(12,10)"></div></td>
                            <td><div id="(13,10)"></div></td>
                            <td><div id="(14,10)"></div></td>
                            <td><div id="(15,10)"></div></td>
                            <td><div id="(16,10)"></div></td>
                            <td><div id="(17,10)"></div></td>
                            <td><div id="(18,10)"></div></td>
                            <td><div id="(19,10)"></div></td>
                            <td><div id="(20,10)"></div></td>
                        </tr>                       

                        <tr>
                        <th>9</th>
                            <td><div id="(0,9)"></div></td>
                            <td><div id="(1,9)"></div></td>
                            <td><div id="(2,9)"></div></td>
                            <td><div id="(3,9)"></div></td>
                            <td><div id="(4,9)"></div></td>
                            <td><div id="(5,9)"></div></td>
                            <td><div id="(6,9)"></div></td>
                            <td><div id="(7,9)"></div></td>
                            <td><div id="(8,9)"></div></td>
                            <td><div id="(9,9)"></div></td>
                            <td><div id="(10,9)"></div></td>
                            <td><div id="(11,9)"></div></td>
                            <td><div id="(12,9)"></div></td>
                            <td><div id="(13,9)"></div></td>
                            <td><div id="(14,9)"></div></td>
                            <td><div id="(15,9)"></div></td>
                            <td><div id="(16,9)"></div></td>
                            <td><div id="(17,9)"></div></td>
                            <td><div id="(18,9)"></div></td>
                            <td><div id="(19,9)"></div></td>
                            <td><div id="(20,9)"></div></td>
                        </tr>                       
                        <tr>
                        <th>8</th>
                            <td><div id="(0,8)"></div></td>
                            <td><div id="(1,8)"></div></td>
                            <td><div id="(2,8)"></div></td>
                            <td><div id="(3,8)"></div></td>
                            <td><div id="(4,8)"></div></td>
                            <td><div id="(5,8)"></div></td>
                            <td><div id="(6,8)"></div></td>
                            <td><div id="(7,8)"></div></td>
                            <td><div id="(8,8)"></div></td>
                            <td><div id="(9,8)"></div></td>
                            <td><div id="(10,8)"></div></td>
                            <td><div id="(11,8)"></div></td>
                            <td><div id="(12,8)"></div></td>
                            <td><div id="(13,8)"></div></td>
                            <td><div id="(14,8)"></div></td>
                            <td><div id="(15,8)"></div></td>
                            <td><div id="(16,8)"></div></td>
                            <td><div id="(17,8)"></div></td>
                            <td><div id="(18,8)"></div></td>
                            <td><div id="(19,8)"></div></td>
                            <td><div id="(20,8)"></div></td>
                        </tr>
                        <tr>
                        <th>7</th>
                            <td><div id="(0,7)"></div></td>
                            <td><div id="(1,7)"></div></td>
                            <td><div id="(2,7)"></div></td>
                            <td><div id="(3,7)"></div></td>
                            <td><div id="(4,7)"></div></td>
                            <td><div id="(5,7)"></div></td>
                            <td><div id="(6,7)"></div></td>
                            <td><div id="(7,7)"></div></td>
                            <td><div id="(8,7)"></div></td>
                            <td><div id="(9,7)"></div></td>
                            <td><div id="(10,7)"></div></td>
                            <td><div id="(11,7)"></div></td>
                            <td><div id="(12,7)"></div></td>
                            <td><div id="(13,7)"></div></td>
                            <td><div id="(14,7)"></div></td>
                            <td><div id="(15,7)"></div></td>
                            <td><div id="(16,7)"></div></td>
                            <td><div id="(17,7)"></div></td>
                            <td><div id="(18,7)"></div></td>
                            <td><div id="(19,7)"></div></td>
                            <td><div id="(20,7)"></div></td>
                        </tr>
                        <tr>
                        <th>6</th>
                            <td><div id="(0,6)"></div></td>
                            <td><div id="(1,6)"></div></td>
                            <td><div id="(2,6)"></div></td>
                            <td><div id="(3,6)"></div></td>
                            <td><div id="(4,6)"></div></td>
                            <td><div id="(5,6)"></div></td>
                            <td><div id="(6,6)"></div></td>
                            <td><div id="(7,6)"></div></td>
                            <td><div id="(8,6)"></div></td>
                            <td><div id="(9,6)"></div></td>
                            <td><div id="(10,6)"></div></td>
                            <td><div id="(11,6)"></div></td>
                            <td><div id="(12,6)"></div></td>
                            <td><div id="(13,6)"></div></td>
                            <td><div id="(14,6)"></div></td>
                            <td><div id="(15,6)"></div></td>
                            <td><div id="(16,6)"></div></td>
                            <td><div id="(17,6)"></div></td>
                            <td><div id="(18,6)"></div></td>
                            <td><div id="(19,6)"></div></td>
                            <td><div id="(20,6)"></div></td>
                        </tr>
                        <tr>
                        <th>5</th>
                            <td><div id="(0,5)"></div></td>
                            <td><div id="(1,5)"></div></td>
                            <td><div id="(2,5)"></div></td>
                            <td><div id="(3,5)"></div></td>
                            <td><div id="(4,5)"></div></td>
                            <td><div id="(5,5)"></div></td>
                            <td><div id="(6,5)"></div></td>
                            <td><div id="(7,5)"></div></td>
                            <td><div id="(8,5)"></div></td>
                            <td><div id="(9,5)"></div></td>
                            <td><div id="(10,5)"></div></td>
                            <td><div id="(11,5)"></div></td>
                            <td><div id="(12,5)"></div></td>
                            <td><div id="(13,5)"></div></td>
                            <td><div id="(14,5)"></div></td>
                            <td><div id="(15,5)"></div></td>
                            <td><div id="(16,5)"></div></td>
                            <td><div id="(17,5)"></div></td>
                            <td><div id="(18,5)"></div></td>
                            <td><div id="(19,5)"></div></td>
                            <td><div id="(20,5)"></div></td>
                        </tr>
                        <tr>
                        <th>4</th>
                            <td><div id="(0,4)"></div></td>
                            <td><div id="(1,4)"></div></td>
                            <td><div id="(2,4)"></div></td>
                            <td><div id="(3,4)"></div></td>
                            <td><div id="(4,4)"></div></td>
                            <td><div id="(5,4)"></div></td>
                            <td><div id="(6,4)"></div></td>
                            <td><div id="(7,4)"></div></td>
                            <td><div id="(8,4)"></div></td>
                            <td><div id="(9,4)"></div></td>
                            <td><div id="(10,4)"></div></td>
                            <td><div id="(11,4)"></div></td>
                            <td><div id="(12,4)"></div></td>
                            <td><div id="(13,4)"></div></td>
                            <td><div id="(14,4)"></div></td>
                            <td><div id="(15,4)"></div></td>
                            <td><div id="(16,4)"></div></td>
                            <td><div id="(17,4)"></div></td>
                            <td><div id="(18,4)"></div></td>
                            <td><div id="(19,4)"></div></td>
                            <td><div id="(20,4)"></div></td>
                        </tr>
                        <tr>
                        <th>3</th>
                            <td><div id="(0,3)"></div></td>
                            <td><div id="(1,3)"></div></td>
                            <td><div id="(2,3)"></div></td>
                            <td><div id="(3,3)"></div></td>
                            <td><div id="(4,3)"></div></td>
                            <td><div id="(5,3)"></div></td>
                            <td><div id="(6,3)"></div></td>
                            <td><div id="(7,3)"></div></td>
                            <td><div id="(8,3)"></div></td>
                            <td><div id="(9,3)"></div></td>
                            <td><div id="(10,3)"></div></td>
                            <td><div id="(11,3)"></div></td>
                            <td><div id="(12,3)"></div></td>
                            <td><div id="(13,3)"></div></td>
                            <td><div id="(14,3)"></div></td>
                            <td><div id="(15,3)"></div></td>
                            <td><div id="(16,3)"></div></td>
                            <td><div id="(17,3)"></div></td>
                            <td><div id="(18,3)"></div></td>
                            <td><div id="(19,3)"></div></td>
                            <td><div id="(20,3)"></div></td>
                        </tr>
                        <tr>
                        <th>2</th>
                            <td><div id="(0,2)"></div></td>
                            <td><div id="(1,2)"></div></td>
                            <td><div id="(2,2)"></div></td>
                            <td><div id="(3,2)"></div></td>
                            <td><div id="(4,2)"></div></td>
                            <td><div id="(5,2)"></div></td>
                            <td><div id="(6,2)"></div></td>
                            <td><div id="(7,2)"></div></td>
                            <td><div id="(8,2)"></div></td>
                            <td><div id="(9,2)"></div></td>
                            <td><div id="(10,2)"></div></td>
                            <td><div id="(11,2)"></div></td>
                            <td><div id="(12,2)"></div></td>
                            <td><div id="(13,2)"></div></td>
                            <td><div id="(14,2)"></div></td>
                            <td><div id="(15,2)"></div></td>
                            <td><div id="(16,2)"></div></td>
                            <td><div id="(17,2)"></div></td>
                            <td><div id="(18,2)"></div></td>
                            <td><div id="(19,2)"></div></td>
                            <td><div id="(20,2)"></div></td>
                        </tr>
                        <tr>
                        <th>1</th>
                            <td><div id="(0,1)"></div></td>
                            <td><div id="(1,1)"></div></td>
                            <td><div id="(2,1)"></div></td>
                            <td><div id="(3,1)"></div></td>
                            <td><div id="(4,1)"></div></td>
                            <td><div id="(5,1)"></div></td>
                            <td><div id="(6,1)"></div></td>
                            <td><div id="(7,1)"></div></td>
                            <td><div id="(8,1)"></div></td>
                            <td><div id="(9,1)"></div></td>
                            <td><div id="(10,1)"></div></td>
                            <td><div id="(11,1)"></div></td>
                            <td><div id="(12,1)"></div></td>
                            <td><div id="(13,1)"></div></td>
                            <td><div id="(14,1)"></div></td>
                            <td><div id="(15,1)"></div></td>
                            <td><div id="(16,1)"></div></td>
                            <td><div id="(17,1)"></div></td>
                            <td><div id="(18,1)"></div></td>
                            <td><div id="(19,1)"></div></td>
                            <td><div id="(20,1)"></div></td>
                        </tr>
                        <tr>
                        <th>0</th>
                            <td><div id="(0,0)"></div></td>
                            <td><div id="(1,0)"></div></td>
                            <td><div id="(2,0)"></div></td>
                            <td><div id="(3,0)"></div></td>
                            <td><div id="(4,0)"></div></td>
                            <td><div id="(5,0)"></div></td>
                            <td><div id="(6,0)"></div></td>
                            <td><div id="(7,0)"></div></td>
                            <td><div id="(8,0)"></div></td>
                            <td><div id="(9,0)"></div></td>
                            <td><div id="(10,0)"></div></td>
                            <td><div id="(11,0)"></div></td>
                            <td><div id="(12,0)"></div></td>
                            <td><div id="(13,0)"></div></td>
                            <td><div id="(14,0)"></div></td>
                            <td><div id="(15,0)"></div></td>
                            <td><div id="(16,0)"></div></td>
                            <td><div id="(17,0)"></div></td>
                            <td><div id="(18,0)"></div></td>
                            <td><div id="(19,0)"></div></td>
                            <td><div id="(20,0)"></div></td>
                        </tr>
                    </tbody>
                </table>
                </div>
        )
    }

