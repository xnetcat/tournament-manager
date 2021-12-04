import React from "react"
import axios from "axios"
import Input from "./input"
import Queue from "./queue"
import Score from "./score"

type MainState = {
  player1: {
    name: string,
    score: number
  },
  player2: {
    name: string,
    score: number
  },
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
      player1: {
        name: "",
        score: 0,
      },
      player2: {
        name: "",
        score: 0,
      },
      queue: []
    }
  }

  updateQueue = () => {
    axios.get("http://localhost:1347/queue")
      .then(res => {
        this.setState({
          queue: res.data
        })
      })
  }

  updateScore = (action: string, playerNumber: number) => {
    axios.post(`http://localhost:1347/game/update/${playerNumber}/${action}`)
    .then(res => {
      if (res.data.success) {
        this.setState({
          player1: {
            name: res.data.player1.name,
            score: res.data.player1.score
          },
          player2: {
            name: res.data.player2.name,
            score: res.data.player2.score
          }
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
    let game;
    if (this.state.queue.length > 0) {
      game = this.state.queue[0]
    }
    else {
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
        <Queue queue={this.state.queue} updateCallback={this.updateQueue} resetCallback={this.resetQueue} />
        <Input />
      </div>
    )
  }
}

export default Main;