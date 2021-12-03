import sys
import json
from typing import Literal
from fastapi import FastAPI, APIRouter
from pathlib import Path
import fastapi
from fastapi.staticfiles import StaticFiles
import uvicorn
import requests
from functools import wraps


SERVER = "http://localhost:8080/" if "--dev" in sys.argv else ""
DEFAULT_CONFIG = {
    "key_bindings": {
        "increment": "ctrl+up",
        "decrement": "ctrl+down",
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
    

_api_routes_registry = []
class api_route(object):
    def __init__(self, path, **kwargs):
        self._path = path
        self._kwargs = kwargs

    def __call__(self, fn):
        cls, method = fn.__repr__().split(" ")[1].split(".")
        _api_routes_registry.append(
            {
                "fn": fn,
                "path": self._path,
                "kwargs": self._kwargs,
                "cls": cls,
                "method": method,
            }
        )

        @wraps(fn)
        def decorated(*args, **kwargs):
            return fn(*args, **kwargs)

        return decorated

    @classmethod
    def add_api_routes(cls, router):
        for reg in _api_routes_registry:
            if router.__class__.__name__ == reg["cls"]:
                router.add_api_route(
                    path=reg["path"],
                    endpoint=getattr(router, reg["method"]),
                    **reg["kwargs"],
                )

fastapi = FastAPI()
class ItemRouter(APIRouter):
    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)
        api_route.add_api_routes(self)
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

        self.player1_score_file = player1_score_file
        self.player2_score_file = player2_score_file
        self.player1_name_file = player1_name_file
        self.player2_name_file = player2_name_file
        self.host_mode = host_mode
        self.settings = settings

    @api_route("/tournament", methods=["GET"])
    def read_tournament(self):
        """
        Returns the current tournament.
        """

        return requests.get(f"{SERVER}tournament").json()

    @api_route("/load", methods=["POST"])
    def load_tournament(self, url: str):
        """
        Loads a tournament from a given url.
        """

        return requests.post(f"{SERVER}load", params={"url": url}).json()

    @api_route("/game/{player}/{action}", methods=["POST"])
    def increment_score(self, player: Literal["1","2"], action: Literal["increment", "decrement"]):
        """
        Increment or decrement the score of a specified player    
        """

        resp = requests.post(f"{SERVER}game/{player}/{action}").json()
        if resp["status"] == "success":
            with open(self.settings[f"player{player}"]["score"], "w") as f:
                f.write(str(resp["score"]))

            with open(self.settings[f"player{player}"]["name"], "rw") as f:
                if f.read() != resp[f"player{player}"]["name"]:
                    f.write(resp[f"player{player}"]["name"])
            
        return resp

    @api_route("/current_game", methods=["GET"])
    def get_current_game():
        """
        Returns the current game.
        """

        return requests.get(f"{SERVER}current_game").json()

if "--dev" in sys.argv:
    fastapi.mount("/", StaticFiles(directory="build", html=True), name="site")

if __name__ == "__main__":
    fastapi.include_router(ItemRouter())
    uvicorn.run(fastapi, host="127.0.0.1", port=8080) # type: ignore