import React from "react"
import axios from "axios"
import Input from "./input"
import Queue from "./queue"
import Score from "./score"

type MainState = {
  queue: {
    player1: {
      name: string,
      score: number
    },
    player2: {
      name: string,
      score: number
    }
  }[],
}

class Main extends React.Component<{}, MainState> {
  constructor(props: {}) {
    super(props)
    this.state = {
      queue: []
    }
  }

  updateQueue = () => {
    axios.get("http://localhost:1347/queue")
      .then(res => {
        if (this.state.queue != res.data) {
          this.setState({
            queue: res.data
          })
        }
      })
  }

  updateScore = (action: string, playerNumber: number) => {
    axios.post(`http://localhost:1347/game/update/${playerNumber}/${action}`)
    .then(res => {
      if (res.data.success) {
        this.updateQueue();
      }
    })
  }

  loadQueue = (url: string) => {
    axios.post("http://localhost:1347/queue/load", null, {params: {url: url}})
      .then(res => {
        if (res.data.success) {
          this.setState({
            queue: res.data.queue
          })
        }
      })
  }

  resetQueue = () => {
    axios.post("http://localhost:1347/queue/reset")
      .then(res => {
        if (res.data.success == true) {
          this.setState({
            queue: []
          })
        }
      })
  }

  componentDidMount() {
    setInterval(this.updateQueue, 500);
  };

  render() {
    let game = this.state.queue.shift();

    if (!game) {
      game = {
        player1: {
          name: "",
          score: 0
        },
        player2: {
          name: "",
          score: 0
        }
      };
    }
    return (
      <div>
        <Score player1={game.player1} player2={game.player2} onScoreChange={this.updateScore}/>
        <Queue queue={this.state.queue} updateCallback={this.updateQueue} resetCallback={this.resetQueue} loadCallback={this.loadQueue} />
        <Input />
      </div>
    )
  }
}

export default Main;