# a flask webserver that encapsulates a gomoku ai (as example a simple random AI)
from flask import Flask, request, json, Response
from bson import json_util
import logging

import random, time

logging.basicConfig(filename="mylog.log")
app = Flask(__name__)


@app.route("/make_gomoku_move/ai_random", methods=["POST"])
def make_gomoku_move_9g3():
    # IncrementalStringDecode

    data = request.json
    ar_error = []

    if data is None or data == {}:
        ar_error.append("data missing")
        strAllErrors = ""
        for strError in ar_error:
            strAllErrors += strError
        return Response(
            response=json.dumps({"Error": strError}),
            status=400,
            mimetype="application/json",
        )

    gomoku_ai = gomoku_random_ai_webServer()
    move = gomoku_ai.move(data)

    # dicResponse,ar_error = temptest(data)
    # if(len(ar_error)!=0): return MongoAPI.returnErrors(ar_error)
    dicResponse = {}
    dicResponse["move"] = move
    return Response(
        response=json_util.dumps(dicResponse), status=200, mimetype="application/json"
    )


# ******************************************************
# End of Flask part.  Below is the AI part.
# ******************************************************


class GmGameRules:
    winningSeries = 5  # global class variable. will be overridden below.
    BOARDWIDTH = 19
    BOARDHEIGHT = 19


def isValidMove(board, column, row):
    # Returns True if there is an empty space in the given column.
    # Otherwise returns False.
    return (
        (column >= 0)
        and (column < len(board))
        and (row >= 0)
        and (row < len(board[0]))
        and (board[column][row] == 0)
    )


def getRandomMove(board):
    # let's make a random move
    # First, make a list of all empty spots
    validMoves = []
    for col in range(GmGameRules.BOARDWIDTH):
        for row in range(GmGameRules.BOARDHEIGHT):
            if isValidMove(board, col, row):
                validMoves.append((col, row))

    return random.choice(validMoves)


# player gives an implementation the basePlayer cl
class randomPlayer:
    def __init__(self, black_=True):
        self.black = black_

        self.max_move_time_ns = 0
        self.start_time_ns = 0

    def new_game(self, black_):
        self.black = black_

    def move(self, gamestate, last_move, max_time_to_move=1000):
        board = gamestate[0]
        # ply=gamesate[1]

        self.max_move_time_ns = 0.95 * max_time_to_move * 1000000  # ms to ns
        self.start_time_ns = time.time_ns()

        return getRandomMove(board)

    def id(self):
        return "Marius"


class gomoku_random_ai_webServer:
    def move(self, dic):
        # strData=strUrlEncodedData # urllib.parse.unquote(strUrlEncodedData)

        # dic=json.loads(strData)

        GmGameRules.winningSeries = dic["winningSeries"]
        GmGameRules.BOARDWIDTH = dic["boardSize"]
        GmGameRules.BOARDHEIGHT = dic["boardSize"]

        gamestate = (dic["board"], dic["ply"])
        last_move = dic["last_move"]
        # we'll deriver valid_moves ourselves
        player = randomPlayer(dic["black"])

        return player.move(gamestate, last_move, dic["max_time_to_move"])
