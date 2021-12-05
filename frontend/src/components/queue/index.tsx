import axios from "axios";
import React from "react";

type QueueProps = {
    queue: {
        player1: {
            name: string,
            score: number,
        },
        player2: {
            name: string,
            score: number,
        },
    }[],
    updateCallback: () => void,
    resetCallback: () => void,
    loadCallback: (url: string) => void,
}

class Queue extends React.Component<QueueProps, {}> {
    constructor(props: QueueProps) {
        super(props);
    }

    clickHandler = (event: React.FormEvent<HTMLButtonElement>) => {
        event.preventDefault();
        const url = prompt("Enter the url of the tournament");
        if (url) {
            if (url.match(/https\:\/\/play\.toornament.com\/[a-z]+_[A-Z]+\/tournaments\/\w{19}\/stages\/\w{19}\//g)) {
                this.props.loadCallback(url);
                return;
            }
        }

        alert("Invalid url");
    }

    changeMaxScore = (event: React.FormEvent<HTMLButtonElement>) => {
        event.preventDefault();
        const maxScore = prompt("Enter the max score");
        if (maxScore) {
            const score = parseInt(maxScore);
            if (score > 0) {
                axios.post("http://localhost:1347/change_max_score", null, {
                    params: {
                        
                        max_score: score,
                    }
                })
                return;
            }            
        }
        alert("Invalid score");
        return;
    }

    render() {
        return (
            <div className="flex flex-col justify-between" style={{height: "80vh"}}>
                <div className="space-x-5 flex items-center justify-center text-center">
                    <table className="w-full">
                        <thead className="w-full">
                            <tr className="w-full">
                                <th className="w-1/2">Player 1</th>
                                <th className="w-1/2">Player 2</th>
                            </tr>
                        </thead>
                        <tbody>
                            {
                                this.props.queue.map((item, index) => {
                                    return (
                                        <tr key={index} >
                                            <td className="w-1/2">{item.player1.name}</td>
                                            <td className="w-1/2">{item.player2.name}</td>
                                        </tr>
                                    )
                                })
                            }
                        </tbody>
                    </table>
                </div>

                <div className="space-x-5 flex items-center justify-center text-center">
                    <button className="h-10 w-32 bg-blue-700 rounded-md border-none" onClick={this.props.updateCallback}>Update</button>
                    <button className="h-10 w-32 bg-blue-700 rounded-md border-none" onClick={this.props.resetCallback}>Reset</button>
                    <button className="h-10 w-32 bg-blue-700 rounded-md border-none" onClick={this.clickHandler}>Load</button>
                    <button className="h-10 w-32 bg-blue-700 rounded-md border-none text-sm" onClick={this.changeMaxScore}>Change max score</button>
                </div>
            </div>
        );
    }

}

export default Queue;