import sys
import json
import keyboard
import uvicorn
import requests

from typing import Literal
from fastapi import FastAPI
from pathlib import Path
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware

DEFAULT_CONFIG = {
    "key_bindings": {
        1: {
            "increment": "ctrl+F9",
            "decrement": "ctrl+F10",
        },
        2: {
            "increment": "ctrl+F11",
            "decrement": "ctrl+F12",
        },
        "reset": "ctrl+r",
    },
    "player1": {
        "name": "player1_name.txt",
        "score": "player1_score.txt",
    },
    "player2": {
        "name": "player2_name.txt",
        "score": "player2_score.txt",
    },
    "url": "http://localhost:8000",
    "is_host": True,
}

app = FastAPI()
settings = {}

config_file = Path("config.json")
if config_file.exists():
    with open("config.json") as f:
        config = json.load(f)
else:
    config = {}

for key in DEFAULT_CONFIG.keys():
    if config.get(key) is None:
        settings[key] = DEFAULT_CONFIG[key]
    else:
        settings[key] = config[key]


@app.get("/queue")
def get_queue():
    """
    Returns the current queue.
    """

    return requests.get(f"{settings['url']}/queue").json()


@app.post("/queue/load")
def load_queue(url: str):
    """
    Loads a queue from a given url.
    """

    return requests.post(f"{settings['url']}/queue/load", params={"url": url}).json()


@app.post("/queue/add")
def add_game(player1Name: str, player2Name: str):
    """
    Adds a new game to queue.
    """

    return requests.post(f"{settings['url']}/queue/add", params={
        "player1Name": player1Name,
        "player2Name": player2Name,
    }).json()


@app.post("/queue/reset")
def reset_queue():
    """
    Resets the queue.
    """

    return requests.post(f"{settings['url']}/queue/reset").json()


@app.get("/game")
def get_current_game():
    """
    Returns the current game.
    """

    return requests.get(f"{settings['url']}/game").json()


@app.post("/game/update/{player}/{action}")
def update_game(player: int, action: Literal["increment", "decrement"]):
    """
    Increment or decrement the score of a specified player    
    """

    resp = requests.post(
        f"{settings['url']}/game/update/{player}/{action}").json()
    if settings["is_host"]:
        if resp["success"] == True:
            with open(settings["player{player}"]["score"], "w") as f:
                f.write(str(resp[f"player{player}"]["score"]))

            with open(settings[f"player{player}"]["name"], "w") as f:
                f.write(resp[f"player{player}"]["name"])

    return resp


@app.post("/game/reset")
def reset_game():
    return requests.post(f"{settings['url']}/game/reset").json()


if "--dev" not in sys.argv:
    app.mount("/", StaticFiles(directory="build", html=True), name="site")
else:
    origins = [
        "http://localhost",
        "http://localhost:3000",
    ]

    app.add_middleware(
        CORSMiddleware,
        allow_origins=origins,
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

if __name__ == "__main__":
    for key in settings["key_bindings"].keys():
        if key == "reset":
            keyboard.add_hotkey(settings["key_bindings"][key], reset_game)
            continue

        for action in settings["key_bindings"][key].keys():
            keyboard.add_hotkey(
                settings["key_bindings"][key][action], update_game, args=(int(key), action))

    uvicorn.run(app, host="127.0.0.1", port=1347)  # type: ignore
