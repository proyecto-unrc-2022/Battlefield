import React, { Component } from "react";

import UserService from "../services/user.service";

export default class Home extends Component {
  constructor(props) {
    super(props);

    this.state = {
      content: null,
    };
  }

  componentDidMount() {
    UserService.getPublicContent().then(
      (response) => {
        this.setState({
          content: response.data,
        });
      },
      (error) => {
        this.setState({
          content:
            (error.response && error.response.data) ||
            error.message ||
            error.toString(),
        });
      }
    );
  }

  render() {
    if (!!this.state || !!this.state.content){
      return "There are o Players"
    }
    const listItems =
      this.state.content &&
      this.state.content.map((u) => <li key={u.id}>{u.username}</li>);

    return (
      <div className="container">
        <header className="jumbotron">
          <h3>Players</h3>
          <ul>{listItems}</ul>
        </header>
      </div>
    );
  }
}
