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
}

class Queue extends React.Component<QueueProps, {}> {
    constructor(props: QueueProps) {
        super(props);
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

                <div className="space-x-5 flex items-center justify-center">
                    <button className="h-10 w-32 bg-blue-700 rounded-md border-none" onClick={this.props.updateCallback}>Update</button>
                    <button className="h-10 w-32 bg-blue-700 rounded-md border-none" onClick={this.props.resetCallback}>Reset</button>
                </div>
            </div>
        );
    }

}

export default Queue;