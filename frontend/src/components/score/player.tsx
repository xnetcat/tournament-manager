import React from 'react';

type PlayerProps = {
    name: string,
    playerNumber: number,
    onScoreChange: (action: string, playerNumber: number) => void,
}

type PlayerState = {
    name: string,
    playerNumber: number
}

class Player extends React.Component<PlayerProps, PlayerState> {
    constructor(props: PlayerProps | Readonly<PlayerProps>) {
        super(props);
        this.state = {
            name: props.name,
            playerNumber: props.playerNumber,
        };
    }

    render() {
        return (
            <div className="player">
                {
                    this.state.playerNumber == 1 ?
                    <div>
                    <div className="player-buttons">
                        <button onClick={() => this.props.onScoreChange("increment", this.state.playerNumber)}>+</button>
                        <button onClick={() => this.props.onScoreChange("decrement", this.state.playerNumber)}>-</button>
                    </div>
                    <div className="player-name">
                        {this.state.name}
                    </div>
                    </div>
                    :
                    <div>
                    <div className="player-name">
                        {this.state.name}
                    </div>
                    <div className="player-buttons">
                        <button onClick={() => this.props.onScoreChange("increment", this.state.playerNumber)}>+</button>
                        <button onClick={() => this.props.onScoreChange("decrement", this.state.playerNumber)}>-</button>
                    </div>
                    </div>
                }   
            </div>
        );
    }

}

export default Player;