import React from "react";
import axios from "axios";

type InputState = {
    player1Name: string | null,
    player2Name: string | null
}

class Input extends React.Component<{}, InputState> {
    constructor(props: any) {
        super(props);
        this.state = {
            player1Name: null,
            player2Name: null
        };
    };

    handlePlayer1Change = (event: React.ChangeEvent<HTMLInputElement>) => {
        this.setState({
            player1Name: event.target.value
        });
    };

    handlePlayer2Change = (event: React.ChangeEvent<HTMLInputElement>) => {
        this.setState({
            player2Name: event.target.value
        });
    };

    handleSubmit = (event: React.FormEvent<HTMLButtonElement>) => {
        event.preventDefault();

        axios.post("http://localhost:1347/queue/add", null, {
            params: {
                "player1Name": this.state.player1Name,
                "player2Name": this.state.player2Name
            }
        })
    };

    render() {
        return (
            <div className="space-x-5 flex justify-center p-2" style={{height: "7vh"}}>
                <input className="rounded-md border-opacity-50 bg-gray-600 border-blue-500 text-center border-2 w-32 h-10" type="text" placeholder="username1" onChange={this.handlePlayer1Change} />
                <button className="rounded-md border-none bg-blue-700 text-center border-2 w-32 h-10" onClick={this.handleSubmit}>Submit</button>
                <input className="rounded-md border-opacity-50 bg-gray-600 border-blue-500 text-center border-2 w-32 h-10" type="text" placeholder="username2" onChange={this.handlePlayer2Change} />
            </div>
        );
    };
};

export default Input;