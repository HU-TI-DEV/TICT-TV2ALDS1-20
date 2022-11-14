from gomoku import SIZE

# change the rules for testing
# reasonable combinations for pureMontecarlo are: w=8,h=8,series=5, rollouts(in move = 8000 / time=4s)
# kies hoogte en breedte gelijk
class GmGameRules:
    winningSeries = 5  # 5 for Gomoku
    BOARDWIDTH = SIZE  # 19 for Gomoku   Select it in gomuku.py, to keep synced with
    BOARDHEIGHT = SIZE  # 19 for Gomoku   agents that call its member functions.
