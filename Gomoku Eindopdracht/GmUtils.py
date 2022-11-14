import random
from GmGameRules import GmGameRules
from gomoku import Move, GameState

# This default base player does a randomn move
class basePlayer:
    """This class specifies a player that just does random moves.
    The use of this class is two-fold: 1) You can use it as a base random roll-out policy.
    2) it specifies the required methods that will be used by the competition to run
    your player
    """

    def __init__(self, black_: bool = True):
        """Constructor for the player."""
        self.black = black_

    def new_game(self, black_: bool):
        """At the start of each new game you will be notified by the competition.
        this method has a boolean parameter that informs your agent whether you
        will play black or white.
        """
        self.black = black_

    def move(
        self, state: GameState, last_move: Move, max_time_to_move: int = 1000
    ) -> Move:
        """This is the most important method: the agent will get:
        1) the current state of the game
        2) the last move by the opponent
        3) the available moves you can play (this is a special service we provide ;-) )
        4) the maximum time until the agent is required to make a move in milliseconds [diverging from this will lead to disqualification].
        """
        moves = GmUtils.getValidMoves(state[0])
        return random.choice(moves)

    def id(self) -> str:
        """Please return a string here that uniquely identifies your submission e.g., "name (student_id)" """
        return "random_player"


class GmUtils:
    @staticmethod
    def getNonActivePlayer(activePlayer, player1, player2):
        return player1 if id(activePlayer) == id(player2) else player2

    @staticmethod
    def isWinningMove(last_move, board):
        """This method checks whether the last move played wins the game.
        The rule for winning is: /exactly/ 5 stones line up (so not 6 or more),
        horizontally, vertically, or diagonally."""
        bsize = len(board)
        assert len(board[0]) == bsize  # verify the assumption made below.
        color = board[last_move[0]][last_move[1]]
        # check up-down
        number_ud = 1
        if last_move[1] < bsize - 1:
            lim1 = last_move[1] + 1
            lim2 = (
                last_move[1] + GmGameRules.winningSeries + 1
                if last_move[1] + GmGameRules.winningSeries + 1 < bsize
                else bsize
            )
            for i in range(lim1, lim2):
                if board[last_move[0]][i] == color:
                    number_ud += 1
                else:
                    break
        if last_move[1] > 0:
            lim2 = (
                last_move[1] - GmGameRules.winningSeries
                if last_move[1] - GmGameRules.winningSeries > 0
                else 0
            )
            for i in reversed(range(lim2, last_move[1])):
                if board[last_move[0]][i] == color:
                    number_ud += 1
                else:
                    break
        if (
            number_ud >= GmGameRules.winningSeries
        ):  # TODO: use == for gomoku (and >= for 5 in a row)
            return True
        # check left - right
        number_lr = 1
        if last_move[0] < bsize - 1:
            lim1 = last_move[0] + 1
            lim2 = (
                last_move[0] + GmGameRules.winningSeries + 1
                if last_move[0] + GmGameRules.winningSeries + 1 < bsize
                else bsize
            )
            for i in range(lim1, lim2):
                if board[i][last_move[1]] == color:
                    number_lr += 1
                else:
                    break
        if last_move[0] > 0:
            lim2 = (
                last_move[0] - GmGameRules.winningSeries
                if last_move[0] - GmGameRules.winningSeries > 0
                else 0
            )
            for i in reversed(range(lim2, last_move[0])):
                if board[i][last_move[1]] == color:
                    number_lr += 1
                else:
                    break
        if (
            number_lr >= GmGameRules.winningSeries
        ):  # TODO: use == for gomoku (and >= for 5 in a row)
            return True
        # check lower left - upper right
        number_diag = 1
        xlim = last_move[0] - 1
        ylim = last_move[1] - 1
        while xlim >= 0 and ylim >= 0:
            if board[xlim][ylim] == color:
                number_diag += 1
            else:
                break
            xlim = xlim - 1
            ylim = ylim - 1
        xlim = last_move[0] + 1
        ylim = last_move[1] + 1
        while xlim < bsize and ylim < bsize:
            if board[xlim][ylim] == color:
                number_diag += 1
            else:
                break
            xlim = xlim + 1
            ylim = ylim + 1
        if (
            number_diag >= GmGameRules.winningSeries
        ):  # TODO: use == for gomoku (and >= for 5 in a row)
            return True
        # check lower right - upper left
        number_diag = 1
        xlim = last_move[0] + 1
        ylim = last_move[1] - 1
        while xlim < bsize and ylim >= 0:
            if board[xlim][ylim] == color:
                number_diag += 1
            else:
                break
            xlim = xlim + 1
            ylim = ylim - 1
        xlim = last_move[0] - 1
        ylim = last_move[1] + 1
        while xlim >= 0 and ylim < bsize:
            if board[xlim][ylim] == color:
                number_diag += 1
            else:
                break
            xlim = xlim - 1
            ylim = ylim + 1
        if (
            number_diag >= GmGameRules.winningSeries
        ):  # TODO: use == for gomoku (and >= for 5 in a row)
            return True
        return False

    @staticmethod
    def isValidMove(board, row, col):
        # Returns True if there is an empty space in the given column.
        # Otherwise returns False.
        return (
            (row >= 0)
            and (row < len(board))
            and (col >= 0)
            and (col < len(board[0]))
            and (board[row][col] == 0)
        )

    @staticmethod
    def addMoveToBoard(board, move, color):
        board[move[0]][move[1]] = color

    @staticmethod
    def removeTokenFromBoard(board, move):
        board[move[0]][move[1]] = 0  # 0 must mean empty, for this.

    @staticmethod
    def getValidMoves(board, ply):
        # First, make a list of all empty spots
        validMoves = []

        centerRow = (len(board)) // 2
        centerCol = (len(board[0])) // 2
        firstMove = (centerRow, centerCol)

        if ply == 1:  # last_move==None:
            # do the first move
            validMoves.append(firstMove)
            return validMoves

        for row in range(0, len(board)):
            for col in range(0, len(board[0])):
                if GmUtils.isValidMove(board, row, col):
                    tup = (row, col)
                    if tup != firstMove:
                        validMoves.append(tup)

        # if we're the black player, then we cannot move our SECOND move anywhere at a distance of 1 or 2 tiles from the center.
        # .. unless we're testing with a board of size 5 or smaller

        # nov 2021: commented out the part below, because we have abolished the second move rule.
        # if (ply==3) and (GmGameRules.BOARDWIDTH>7):
        #     # we're black, and it's our second move.
        #     # we are not allowed to play our second move near the center.
        #     centerX = (len(board)) // 2
        #     centerY =(len (board[0])) // 2
        #     for y in range(centerY-2,centerY+3):
        #         for x in range(centerX-2,centerX+3):
        #             try:
        #                 validMoves.remove((x,y))
        #             except:
        #                 dummy=1;dummy=dummy

        return validMoves
