import React, { Component } from "react";
import { Routes, Route, Link } from "react-router-dom";
import "bootstrap/dist/css/bootstrap.min.css";
import "./App.css";

import AuthService from "./services/auth.service";

import Login from "./components/login.component";
import Home from "./components/home.component";
// import Profile from "./components/profile.component";
import Board from "./components/board.component";
import NavyMenu from "./navy/pages/NavyMenu";
import NavyGames from "./navy/pages/NavyGames";
import UnderRoot from "./underwater/UnderRoot";
import UnderMenu from "./underwater/UnderMenu";
import UnderGame from "./underwater/UnderGame";
import UnderHome from "./underwater/UnderHome";
import UnderNewGame from "./underwater/UnderNewGame";
import UnderJoinGame from "./underwater/UnderJoinGame";
import NavyShipSelection from "./navy/pages/NavyShipSelection";
import { NavyShipPlace } from "./navy/pages/NavyShipPlace";
import NavyLobby from "./navy/pages/NavyLobby"
import NavyBoard from "./navy/pages/NavyBoard";
import NavyHowToPlay from "./navy/pages/NavyHowToPlay";

//Borrar esto y la route
import HomePage from "./infantry/pages/HomePage";
import CreateGame from "./infantry/pages/CreateGame"
import JoinGame from "./infantry/pages/JoinGame"
import GameInfantry from "./infantry/components/gameInfantry.component";
import ChooseCharacter from "./infantry/pages/ChooseCharacter";
import WaitPlayer from "./infantry/pages/WaitPlayer";



import AirforceAPP from "./airforce/AirforceAPP";
import ChoosePlane from "./airforce/components/AirforceChoosePlane.component";
import AirforceLobby from "./airforce/components/AirforceLobby.component"
import NavySpectateBoard from "./navy/pages/NavySpectateBoard";

import AirforceBoard from "./airforce/components/AirforceBoard.component";
import GameRoom from "./airforce/components/AirforceGameRoom.component";
class App extends Component {
  constructor(props) {
    super(props);
    this.logOut = this.logOut.bind(this);

    this.state = {
      currentUser: undefined,
    };
  }

  componentDidMount() {
    const user = AuthService.getCurrentUser();

    if (user) {
      this.setState({
        currentUser: [user],
      });
    }
  }

  logOut() {
    AuthService.logout();
    this.setState({
      currentUser: undefined,
    });
  }

  render() {
    const { currentUser } = this.state;

    return (
      <div className="min-vh-100 d-flex flex-column">
        <nav className="navbar navbar-expand navbar-dark bg-dark">
          <Link to={"/"} className="navbar-brand">
            Battlefield
          </Link>
          <div className="navbar-nav mr-auto">
            <li className="nav-item">
              <Link to={"/home"} className="nav-link">
                Home
              </Link>
            </li>

            <li className="nav-item">
              <Link to={"/airforce/mainMenu"} className="nav-link">
                Airforce
              </Link>
            </li>

            {currentUser && (
              <li className="nav-item">
                <Link to={"/user"} className="nav-link">
                  User
                </Link>
              </li>
            )}

            {currentUser && (
              <li className="nav-item">
                <Link to={"/underwater/menu"} className="nav-link">
                  Underwater
                </Link>
              </li>
            )}

            {currentUser && (
              <li className="nav-item">
                <Link to={"/home_Infantry"} className="nav-link">
                Infantry
                </Link>
              </li>
            )}
          

            {currentUser && (
              <li className="nav-item">
                <Link to={"/navy"} className="nav-link">
                  Navy
                </Link>
              </li>
            )}
          </div>

          {currentUser ? (
            <div className="navbar-nav ml-auto">
              <li className="nav-item">
                <Link to={"/profile"} className="nav-link">
                  {currentUser.username}
                </Link>
              </li>
              <li className="nav-item">
                <a href="/login" className="nav-link" onClick={this.logOut}>
                  LogOut
                </a>
              </li>
            </div>
          ) : (
            <div className="navbar-nav ml-auto">
              <li className="nav-item">
                <Link to={"/login"} className="nav-link">
                  Login
                </Link>
              </li>
            </div>
          )}
        </nav>

        <div
          style={{ flexGrow: "1" }}
          className="container-fluid d-flex flex-column p-0"
        >
          <Routes>
            <Route path="/" element={<Home />} />
            <Route path="/home" element={<Home />} />
            <Route path='/home_Infantry/' element={<HomePage/>} />
            <Route path="/home_Infantry/create_game" element={<CreateGame/>} />
            <Route path="/home_Infantry/join_game" element={<JoinGame/>} />
            <Route path="/home_Infantry/choose_character" element={<ChooseCharacter/>} />
            <Route path="/home_Infantry/wait_player" element={<WaitPlayer/>} />
            <Route path="/infantry/game" element={<GameInfantry/>} />
            <Route path="/login" element={<Login />} />
            {/* <Route path="/profile" element={<Profile />} /> */}
            <Route path="/board" element={<Board />} />
            <Route path="/navy" element={<NavyMenu />} />
            <Route path="/navy/games" element={<NavyGames />} />

            <Route path="/underwater" element={<UnderRoot />}>
              <Route path="menu" element={<UnderMenu />}>
                <Route index element={<UnderHome />} />
                <Route path="new" element={<UnderNewGame />} />
                <Route path="lobby" element={<UnderJoinGame />} />
              </Route>
              <Route path="game/:id" element={<UnderGame />} />
            </Route>

            <Route
              path="/navy/games/:id/ship_selection"
              element={<NavyShipSelection />}
            />
            <Route
              path="/navy/games/:id/ship_selection/place_ship"
              element={<NavyShipPlace />}
            />

            <Route path="/navy/games/:id/lobby" element={<NavyLobby />} />
            <Route path="/navy/games/:id/board" element={<NavyBoard />} />
            <Route path="/navy/how_to_play" element={<NavyHowToPlay />} />
            <Route path="/navy/games/:id/spectate_board" element={<NavySpectateBoard />} />
            <Route path= "/airforce/mainMenu" element={<AirforceAPP />}/>
            <Route path= "/airforce/game/lobby/:id" element={<AirforceLobby />}/>
            <Route path= "/airforce/game/:id/choose/plane" element={<ChoosePlane />}/>
            <Route path= "/airforce/game/:id/gameRoom" element={<GameRoom />}/>
          </Routes>
        </div>
      </div>
    );
  }
}

export default App;

