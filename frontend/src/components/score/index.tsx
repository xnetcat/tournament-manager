import React from "react";
import ScoreHeader from "./score";
import Player from "./player";

type ScoreProps = {
    player1: {
        name: string,
        score: number
    },
    player2: {
        name: string,
        score: number
    },
    onScoreChange: (player: string, score: number) => void
}

class Score extends React.Component<ScoreProps, {}> {
    constructor(props: ScoreProps) {
        super(props);
    }

    render() {
        return ( 
            <div className="text-center space-x-10 flex items-center justify-center" style={{height: "10vh"}}>
                <Player name={this.props.player1.name} playerNumber={1} onScoreChange={this.props.onScoreChange} />
                <ScoreHeader player1Score={this.props.player1.score} player2Score={this.props.player2.score}/>
                <Player name={this.props.player2.name} playerNumber={2} onScoreChange={this.props.onScoreChange} />
            </div>
        );
    }
}

export default Score;