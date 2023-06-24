from typing import List, Literal, Optional
from pydantic import BaseModel
from fastapi import FastAPI
import uvicorn
from fastapi.middleware.cors import CORSMiddleware
from bs4 import BeautifulSoup
import requests
import re

class Player(BaseModel):
    name: str
    score: int = 0

class Game(BaseModel):
    player1: Player
    player2: Player
    winner: Optional[Player] = None

class Tournament(BaseModel):
    queue: List[Game] = []
    maxScore: int = 5

app = FastAPI()
tournament = Tournament()

@app.post("/change_max_score")
def change_max_score(max_score: int):
    tournament.maxScore = max_score

    return {"success": True, "max_score": max_score}

@app.post("/queue/load")
def load_tournament(url: str):
    """
    Loads a tournament from a given url.
    """

    regex = re.compile(r"https\:\/\/play\.toornament.com\/[a-z]+_[A-Z]+\/tournaments\/\w{19}\/stages\/\w{19}\/")
    if not regex.match(url):
        return {"success": False ,"error": "Invalid URL"}

    resp = requests.get(url)
    soup = BeautifulSoup(resp.text, "html.parser")

    queue = []
    brackets_node = soup.find("div", {"class": "bracket-nodes"})
    if brackets_node is None:
        return {"success": False ,"error": "No brackets found"}

    for div in brackets_node.find_all("div", recursive=False): # type: ignore
        if 'position: absolute; left: 0rem;' in div["style"]:
            p1 = Player(name=div.find("div", {"class": "opponent opponent-1"}).find("div", {"class": "name"}).get_text().strip())
            p2 = Player(name=div.find("div", {"class": "opponent opponent-2"}).find("div", {"class": "name"}).get_text().strip())
            queue.append(Game(player1=p1, player2=p2))

    tournament.queue = queue
    return {"success": True, "queue": queue}

@app.get("/queue")
def get_queue():
    """
    Returns the current queue.
    """

    return tournament

@app.post("/queue/add")
def add_to_queue(player1Name: str, player2Name: str):
    game = Game(player1=Player(name=player1Name), player2=Player(name=player2Name))
    tournament.queue.append(game)

    return {
        "success": True, 
        "queue": tournament.queue
    }

@app.post("/queue/reset")
def reset_queue():
    tournament.queue = []
    return {
        "success": True, 
        **tournament.dict()
    }

@app.get("/game")
def get_current_game():
    """
    Returns the current game.
    """

    if len(tournament.queue) == 0:
        return {"success": False, "error": "No games in queue"}

    return {
        "success": True, 
        **tournament.queue[0].dict()
    }

@app.post("/game/next")
def next_game():
    """
    Removes the current game from the queue.
    """

    if len(tournament.queue) == 0:
        return {"success": False, "error": "No games in queue"}

    game = tournament.queue.pop(0)
    return {
        "success": True, 
        "game": game
    }

@app.post("/game/update/{player}/{action}")
def change_score(player: Literal["1","2"], action: Literal["increment", "decrement"]):
    """
    Increment or decrement the score of a specified player    
    """

    if len(tournament.queue) == 0:
        return {"success": False, "error": "No games in queue"}

    current_game = tournament.queue[0]

    if player == "1":
        if action == "increment" and current_game.player1.score < tournament.maxScore:
            current_game.player1.score += 1
        elif action == "decrement":
            current_game.player1.score -= 1
    elif player == "2":
        if action == "increment" and current_game.player2.score < tournament.maxScore:
            current_game.player2.score += 1
        elif action == "decrement":
            current_game.player2.score -= 1

    if current_game.player1.score == tournament.maxScore:
        current_game.winner = current_game.player1
    elif current_game.player2.score == tournament.maxScore:
        current_game.winner = current_game.player2
    else:
        current_game.winner = None

    tournament.queue[0] = current_game

    return {
        "success": True, 
        "winner": current_game.winner, 
        "player1": {
            "name": current_game.player1.name,
            "score": current_game.player1.score
        },
        "player2": {
            "name": current_game.player2.name,
            "score": current_game.player2.score
        }
    }

@app.post("/game/reset")
def reset_current_game():
    """
    Resets the current game.
    """

    if len(tournament.queue) == 0:
        return {"success": False, "error": "No games in queue"}

    current_game = tournament.queue[0]
    current_game.player1.score = 0
    current_game.player2.score = 0
    current_game.winner = None

    tournament.queue[0] = current_game

    return {
        "success": True, 
        "winner": current_game.winner, 
        "player1": {
            "name": current_game.player1.name,
            "score": current_game.player1.score
        },
        "player2": {
            "name": current_game.player2.name,
            "score": current_game.player2.score
        }
    }

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=False,
    allow_methods=["*"],
    allow_headers=["*"],
)

uvicorn.run(app, host="127.0.0.1", port=1347)  # type: ignore