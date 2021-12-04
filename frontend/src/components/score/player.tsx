import React from 'react';

type PlayerProps = {
    name: string,
    playerNumber: number,
    onScoreChange: (action: string, playerNumber: number) => void,
}

class Player extends React.Component<PlayerProps, {}> {
    constructor(props: PlayerProps | Readonly<PlayerProps>) {
        super(props);
    }

    render() {
        return (
            <div className="text-gray-300">
                {
                    this.props.playerNumber == 1 ?
                    <div>
                    <div className="">
                        <button onClick={() => this.props.onScoreChange("increment", this.props.playerNumber)}>+</button>
                        <button onClick={() => this.props.onScoreChange("decrement", this.props.playerNumber)}>-</button>
                    </div>
                    <h2 className="">
                        {this.props.name}
                    </h2>
                    </div>
                    :
                    <div>
                    <h2 className="">
                        {this.props.name}
                    </h2>
                    <div className="">
                        <button onClick={() => this.props.onScoreChange("increment", this.props.playerNumber)}>+</button>
                        <button onClick={() => this.props.onScoreChange("decrement", this.props.playerNumber)}>-</button>
                    </div>
                    </div>
                }   
            </div>
        );
    }

}

export default Player;