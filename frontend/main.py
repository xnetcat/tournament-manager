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

def update_game_resp(player: int, action: Literal["increment", "decrement"]):
    resp = requests.post(f"{settings['url']}/game/{player}/{action}").json()
    if settings["is_host"]:
        if resp["success"] == True:
            write_to_file(settings[f"player{player}"]["score"], str(resp[f"player{player}"]["score"]))

            with open(settings[f"player{player}"]["name"], "w+") as f:
                if f.read() != resp[f"player{player}"]["name"]:
                    f.write(resp[f"player{player}"]["name"])

    return resp 

def tournament_resp():
    return requests.get(f"{settings['url']}/tournament").json()

def load_tournament_resp(url: str):
    return requests.post(f"{settings['url']}/load", params={"url": url}).json()

def game_resp():
    return requests.get(f"{settings['url']}/game").json()

def reset_game_resp():
    return requests.post(f"{settings['url']}/game/reset").json()

def write_to_file(file: str, data: str):
    with open(file, "w") as f:
        f.write(data)

@app.get("/tournament")
def read_tournament():
    """
    Returns the current tournament.
    """

    return tournament_resp()    

@app.post("/tournament/load")
def load_tournament(url: str):
    """
    Loads a tournament from a given url.
    """

    return load_tournament_resp(url)

@app.post("/game/{player}/{action}")
def update_game(player: int, action: Literal["increment", "decrement"]):
    """
    Increment or decrement the score of a specified player    
    """

    return update_game(player, action).json()

@app.get("/game")
def get_current_game():
    """
    Returns the current game.
    """

    return game_resp()
    
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
            keyboard.add_hotkey(settings["key_bindings"][key], reset_game_resp)
            continue

        for action in settings["key_bindings"][key].keys():
            keyboard.add_hotkey(settings["key_bindings"][key][action], update_game_resp, args=(int(key), action))
          
    uvicorn.run(app, host="127.0.0.1", port=1347) # type: ignore