import sys
import json
import keyboard
import fastapi
import uvicorn
import requests

from typing import Literal
from fastapi import FastAPI
from pathlib import Path
from fastapi.staticfiles import StaticFiles

SERVER = "http://localhost:8000/" if "--dev" in sys.argv else ""

def score_resp(player: int, action: Literal["increment", "decrement"]):
    resp = requests.post(f"{SERVER}game/{player}/{action}").json()
    print(resp)
    if resp["success"] == True:
        write_to_file(settings[f"player{player}"]["score"], str(resp[f"player{player}"]["score"]))

        with open(settings[f"player{player}"]["name"], "w+") as f:
            if f.read() != resp[f"player{player}"]["name"]:
                f.write(resp[f"player{player}"]["name"])
    
    return resp 

def tournament_resp():
    return requests.get(f"{SERVER}tournament").json()

def load_resp(url: str):
    return requests.post(f"{SERVER}load", params={"url": url}).json()

def load_current_game():
    return requests.get(f"{SERVER}current_game").json()

def reset_resp():
    return requests.post(f"{SERVER}reset_current_game").json()

def write_to_file(file: str, data: str):
    with open(file, "w") as f:
        f.write(data)

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

player1_score_file = Path(settings["player1"]["score"])
player2_score_file = Path(settings["player2"]["score"])
player1_name_file = Path(settings["player1"]["name"])
player2_name_file = Path(settings["player2"]["name"])

host_mode = (
    player1_score_file.exists() and player2_score_file.exists()
    and player1_name_file.exists() and player2_name_file.exists()
)

@app.get("/tournament")
def read_tournament():
    """
    Returns the current tournament.
    """

    return tournament_resp()    

@app.post("/load")
def load_tournament(url: str):
    """
    Loads a tournament from a given url.
    """

    return load_resp(url)

@app.post("/game/{player}/{action}")
def increment_score(player: int, action: Literal["increment", "decrement"]):
    """
    Increment or decrement the score of a specified player    
    """

    resp = score_resp(player, action).json()
        
    return resp

@app.get("/current_game")
def get_current_game():
    """
    Returns the current game.
    """

    return load_current_game()
    
if "--dev" in sys.argv:
    app.mount("/", StaticFiles(directory="build", html=True), name="site")

if __name__ == "__main__":
    for key in settings["key_bindings"].keys():
        if key == "reset":
            keyboard.add_hotkey(settings["key_bindings"][key], reset_resp)
            continue

        for action in settings["key_bindings"][key].keys():
            keyboard.add_hotkey(settings["key_bindings"][key][action], score_resp, args=(int(key), action))
          
    uvicorn.run(app, host="127.0.0.1", port=1347) # type: ignore