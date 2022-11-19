import React, { Component } from "react";
import authService from "../services/auth.service";

import UserService from "../services/user.service";

export default class BoardUser extends Component {
  constructor(props) {
    super(props);

    this.state = {
      content: "",
    };
  }

  componentDidMount() {
    const currentUser = authService.getCurrentUser()
    UserService.getUserBoard(currentUser.sub).then(
      (response) => {
        this.setState({
          content: response.data,
        });
      },
      (error) => {
        this.setState({
          content:
            (error.response &&
              error.response.data &&
              error.response.data.message) ||
            error.message ||
            error.toString(),
        });
      }
    );
  }

  render() {
    return (
      <div className="container">
        <header className="jumbotron">
          {/* <h3>{this.state.content}</h3> */}
          Hola yo soy...
          {this.state.content && this.state.content.username}
        </header>
      </div>
    );
  }
}
