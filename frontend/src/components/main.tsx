// @ts-nocheck
import React from "react"
import axios from "axios"

export default class Main extends React.Component {
  render() {
    axios.get("http://localhost:1347/tournament").then(res => console.log(res))  
    return (
      "hello"
    )
  }
}
