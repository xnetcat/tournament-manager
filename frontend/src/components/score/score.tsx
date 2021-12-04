import React from "react";

type ScoreProps = {
    player1Score: number;
    player2Score: number;
};

type ScoreState = {
    player1Score: number;
    player2Score: number;
};

class ScoreHeader extends React.Component<ScoreProps, ScoreState> {
    constructor(props: ScoreProps) {
        super(props);
        this.state = {
            player1Score: props.player1Score,
            player2Score: props.player2Score,
        };
    }
    render() {
        return (
            <div className="text-center text-lg font-bold">
                <h1>{this.props.player1Score} : {this.props.player2Score}</h1>
            </div>
        );
    }
}

export default ScoreHeader;