# NB: python version 3.7 or higher is required (else time_ns()) doesn't work

import gomoku
from random_agent import random_dummy_player
from gomoku_ai_marius1_webclient import gomoku_ai_marius1_webclient
from gomoku_ai_random_webclient import gomoku_ai_random_webclient
import random
import time


class Competition:
    """This class runs the competition between the submitted players.
    A player needs to have the new_game(black) and move(board, prev_move, valid_moves_list)
    methods implemented. Players are registered one by one using the register_player method.
    The competition is started using the play_competition method."""

    def __init__(self, bsize_=19):
        """Initialises the competition. The board size (default 19) for the entire competition can be set here."""
        self.players = []
        self.results = []
        self.bsize = bsize_

    def register_player(self, player_):
        """This method registers an AI player that the students have implemented.
        This player needs to be in a separate file."""
        self.players.append(player_)

    def play_competition(self, maxtime_per_move=1000, tolerance=0.05):
        """This method runs the actual competition between the registered players.
        Each player plays each other player twice: once with black and once with white."""
        self.results = []
        mtime = (
            maxtime_per_move * (1.0 + tolerance) * 1000000
        )  # operational maxtime in nanoseconds
        for i in range(len(self.players)):
            self.results.append(
                [0.0] * len(self.players)
            )  # set the results matrix to all zeroes
        for i in range(len(self.players)):
            for j in range(len(self.players)):
                if i == j:
                    continue  # players do not play themselves
                self.players[i].new_game(True)  # player i is black
                self.players[j].new_game(False)  # player j is white
                game = gomoku.starting_state(bsize_=self.bsize)  # initialise the game
                previous_move = ()
                over = False
                while not over:
                    if game[1] % 2 == 1:  # black to move
                        current_player = self.players[i]
                        pid = i
                        pid_other = j
                    else:  # white to move
                        current_player = self.players[j]
                        pid = j
                        pid_other = i
                    random.seed(
                        time.time_ns()
                    )  # just in case the other player has tinkered with random.seed.
                    start_time = time.time_ns()
                    move = current_player.move(
                        game, previous_move, max_time_to_move=maxtime_per_move
                    )
                    stop_time = time.time_ns()
                    # print(str((stop_time-start_time)/1000000)+"/"+str(maxtime_per_move*(1+tolerance)))
                    ok, win, game = gomoku.move(
                        game, move
                    )  # perform the move, and obtain whether the move was valid (ok) and whether the move results in a win
                    previous_move = move
                    # Uncomment the follwing two lines if you want to watch the games unfold slowly:
                    # time.sleep(1)
                    # gomoku.pretty_board(game[0])
                    if (stop_time - start_time) > mtime:
                        # player who made the illegal move should be disqualified. This needs to be done manually.
                        print(
                            "disqualified for exceeding maximum time per move: player "
                            + str(pid)
                        )
                    if not ok:
                        # player who made the illegal move should be disqualified. This needs to be done manually.
                        print("disqualified for illegal move: player " + str(pid))
                        print("on board: ")
                        gomoku.pretty_board(game[0])
                        print(
                            "trying to play: ("
                            + str(move[0])
                            + ","
                            + str(move[1])
                            + ")"
                        )
                        if game[1] % 2 == 1:
                            print("as black")
                        else:
                            print("as white")
                    if win:
                        over = True
                        self.results[pid][pid_other] += 1
                    elif len(gomoku.valid_moves(game)) == 0:
                        # if there are no more valid moves, the board is full and it's a draw
                        over = True
                        self.results[pid][pid_other] += 0.5
                        self.results[pid_other][pid] += 0.5

    def print_scores(self):
        """This method prints the results of the competition to sysout"""
        i = 0
        for line in self.results:
            for res in line:
                print(str(res), end=" ")
            print("[" + self.players[i].id() + ", " + str(sum(line)) + "]")
            i += 1


# Now follows the main script for running the competition
# At present the competition consists of just three random dummy players playing each other
# When the students submit a player file, they should be entered one by one.
game = gomoku.starting_state()

player0 = random_dummy_player()
player1 = gomoku_ai_marius1_webclient()
player2 = gomoku_ai_random_webclient()

comp = Competition()
comp.register_player(player1)
comp.register_player(player2)

nofCompetitions = 1
for i in range(nofCompetitions):
    comp.play_competition()
    comp.print_scores()
