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
                    <div className="flex items-center justify-start space-x-5">
                    <div className="flex items-center justify-center space-x-2">
                        <button className="text-xl w-7 text-center outline-none border-opacity-50 font-bold rounded-md border-blue-400 border-2" onClick={() => this.props.onScoreChange("increment", this.props.playerNumber)}>+</button>
                        <button className="text-xl w-7 text-center outline-none border-opacity-50 font-bold rounded-md border-blue-400 border-2" onClick={() => this.props.onScoreChange("decrement", this.props.playerNumber)}>-</button>
                    </div>
                    <h2 className="w-full">
                        {this.props.name}
                    </h2>
                    </div>
                    :
                    <div className="flex items-start justify-start space-x-5">
                    <h2 className="w-full">
                        {this.props.name}
                    </h2>
                    <div className="flex items-center justify-center space-x-3">
                        <button className="text-xl w-7 text-center outline-none border-opacity-50 font-bold rounded-md border-blue-400 border-2" onClick={() => this.props.onScoreChange("decrement", this.props.playerNumber)}>-</button>
                        <button className="text-xl w-7 text-center outline-none border-opacity-50 font-bold rounded-md border-blue-400 border-2" onClick={() => this.props.onScoreChange("increment", this.props.playerNumber)}>+</button>
                    </div>
                    </div>
                }   
            </div>
        );
    }

}

export default Player;