# import time
import requests
import gomoku

# heuristicalmontecarloplayer_webClient calls the web-based webserver
# via a python flask application.
class gomoku_ai_marius1_webclient:
    def __init__(self, black_=True, winningSeries_=5, boardSize_=gomoku.SIZE):
        self.black = black_
        self.winningSeries = winningSeries_
        self.boardSize = boardSize_

    def new_game(self, black_):
        self.black = black_

    def move(self, gamestate, last_move, max_time_to_move=1000):

        max_webaccess_plus_reply_time_ms = (
            600  # .. I hope the ping will nog exceed 0.6s ..
        )

        # So my server has less time because of the send request en receive response
        # back and forth to Denver, Colorado.
        max_time_for_server_script = max_time_to_move - max_webaccess_plus_reply_time_ms

        # fill a dic with info to post.
        dic = {}
        dic["board"] = self.convertToList(
            gamestate[0]
        )  # lists can be json serialised, opposed to numpy arrays,therefore convert first.
        dic["ply"] = gamestate[1]
        dic["last_move"] = self.convertToIntTuple(
            last_move
        )  # (int8,int8) cannot properly be json serialised
        dic["max_time_to_move"] = max_time_for_server_script
        dic["winningSeries"] = self.winningSeries
        dic["boardSize"] = self.boardSize
        dic["black"] = self.black

        # measure the time spent
        # start_time_ns = time.time_ns()

        # call the server using POST.
        url = "https://themave.pythonanywhere.com/make_gomoku_move/ai_marius1"
        req = requests.post(url, json=dic)

        # print(req.json())

        # time_spent_ns =  time.time_ns()-start_time_ns
        # print(time_spent_ns)

        # json kent geen tuples. Die maakt er arrays van. Dus zelf even converteren naar een tuple.
        return tuple(req.json()["move"])

    def id(self):
        return "Marius"

    def convertToIntTuple(self, tup):
        if tup == None or tup == ():
            return None
        else:
            return (int(tup[0]), int(tup[1]))

    def convertToList(self, board):
        if type(board) == type([]):
            return board  # no conversion needed
        else:  # it must be a numpy array. Convert it to list:
            boardAsList = []
            for row in board:
                lstRow = []
                for number in row:
                    # because e.g. int8 numpy types cannot be json serialised.
                    lstRow.append(
                        int(number)
                    )  # because e.g. int8 numpy types cannot be json serialised.
                boardAsList.append(lstRow)
        return boardAsList
