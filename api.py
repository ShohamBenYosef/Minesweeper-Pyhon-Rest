
from fastapi import FastAPI, HTTPException, Query
from pydantic import BaseModel
from typing import List, Dict
from board import Board
import datetime, json, threading, os, uuid


app = FastAPI()


class ActionRequest(BaseModel):
    x: int
    y: int
    action: str # "open" \ "flag" \ "exit


class score(BaseModel):
    username: str
    status: str # "Win" \ "Lose"
    duration: float
    board_size: str # int x int

"""
game_board = None
scores: List[score] = []
start_time = None
user_name = ""
"""

GAMES: Dict[str, Dict] = {}
SCORES_FILE = "scores.json"
_scores_lock = threading.Lock()

# methods:
def _load_scores() -> List[Dict]:
    if os.path.exists(SCORES_FILE):
        with open(SCORES_FILE, "r") as f:
            try:
                return json.load(f)
            except json.JSONDecodeError:
                return []
    return []

def _append_score(score_dict: Dict) ->None:
    with _scores_lock:
        data = _load_scores()
        data.append(score_dict)
        with open(SCORES_FILE, "w") as f:
            json.dump(data, f, indent=2)


def cell_repr(cell):
    if cell.is_flag:
        return "F"
    if not cell.is_visible:
        return "#"
    if cell.is_mine:
        return "*"
    if cell.neighbor_mines > 0:
        return str(cell.neighbor_mines)
    return " "


def board_repr(board):
    return [[cell_repr(c) for c in r] for r in board.grid]


def _return_state(board: Board, msg: str) -> Dict:
    return {
        "message": msg,
        "board": board_repr(board),
        "game_over": board.game_over,
        "is_won": board.is_won()
    }

def _get_game(game_id: str):
    game = GAMES.get[game_id]
    if not game:
        raise HTTPException(status_code=404, detail="Game not found")
    return game



# games requests
@app.get("/start")
def start_game(username: str, width: int = 5, height: int = 5, mines: int = 4):
    game_board = Board(width, height, mines)
    game_board.generate_board()
    game_id = str(uuid.uuid4())
    GAMES[game_id] = {
        "board": game_board,
        "username": username,
        "start_time": datetime.datetime.now()
    }
    payload = _return_state(game_board, "Game started.")
    payload["game_id"] = game_id
    return payload


@app.get("/board")
def get_board(game_id: str = Query(..., title="Game id")):
    game = _get_game(game_id)
    return _return_state(game["board"],"board updated")

@app.post("/action")
def action(request: ActionRequest, game_id: str = Query(...)):

    game = _get_game(game_id)
    board: Board = game["board"]

    x = request.x
    y = request.y
    action = request.action

    if x < 0 or x >= board.width or y < 0 or y >= board.height:
        raise HTTPException(status_code=400, detail="Invalid coordinates.")


    if action == "open":
        board.reveal_cell(x, y)
        msg = "Cell revealed."

    elif action == "flag":
        board.toggle_flag(x, y)
        msg = "Flag toggled."

    elif action == "exit":
        board.game_over = True
        msg = "Game exited."

    else:
        raise HTTPException(status_code=400, detail="Invalid action.")

    if board.game_over:
        status = "Win" if board.is_won() else "Lose"
        duration = (datetime.datetime.now() - game["start_time"]).total_seconds()
        _append_score({
            "username": game["username"],
            "status": status,
            "duration": duration,
            "board_size": f"{board.width}x{board.height}"
        })

    return _return_state(board, msg)



# scores requests
@app.get("/scores")
def get_scores(username: str):
    data = _load_scores()
    if username:
        data = [s for s in data if s.get("username") == username]
    return data