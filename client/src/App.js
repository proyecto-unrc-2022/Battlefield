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
import NavyShipSelection from "./navy/pages/NavyShipSelection";
import { NavyShipPlace } from "./navy/pages/NavyShipPlace";
import NavyLobby from "./navy/pages/NavyLobby"
import NavyBoard from "./navy/pages/NavyBoard";

import AirforceAPP from "./airforce/AirforceAPP";
import ChoosePlane from "./airforce/components/AirforceChoosePlane";
import AirforceLobby from "./airforce/components/AirforceLobby.component"
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
              <Link to={"/navy"} className="nav-link">
                Navy
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
            <Route path="/login" element={<Login />} />
            {/* <Route path="/profile" element={<Profile />} /> */}
            <Route path="/board" element={<Board />} />
            <Route path="/navy" element={<NavyMenu />} />
            <Route path="/navy/games" element={<NavyGames />} />
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
            <Route path= "/airforce/mainMenu" element={<AirforceAPP />}/>
            <Route path= "/airforce/game/lobby/:id" element={<AirforceLobby />}/>
            <Route path= "/airforce/game/:id/choose/plane" element={<ChoosePlane />}/>
          </Routes>
        </div>
      </div>
    );
  }
}

export default App;
