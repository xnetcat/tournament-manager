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

class Queue extends React.Component<QueueProps, {url: string}> {
    constructor(props: QueueProps) {
        super(props);
        this.state = {
            url: "",
        }
    }

    urlHandler = (event: React.ChangeEvent<HTMLInputElement>) => {
        event.preventDefault();
        this.setState({url: event.target.value});
    }

    clickHandler = (event: React.FormEvent<HTMLButtonElement>) => {
        event.preventDefault();
        if (this.state.url.match(/https\:\/\/play\.toornament.com\/[a-z]+_[A-Z]+\/tournaments\/\w{19}\/stages\/\w{19}\//g)) {
            this.props.loadCallback(this.state.url);
        } else {
            alert("Invalid URL");
        }
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
                    <input className="rounded-md border-opacity-50 bg-gray-600 border-blue-500 text-center border-2 w-32 h-10" onChange={this.urlHandler} type="text" placeholder="https://toornament.com/..." />
                    <button className="h-10 w-32 bg-blue-700 rounded-md border-none" onClick={this.clickHandler}>Load</button>
                </div>
            </div>
        );
    }

}

export default Queue;