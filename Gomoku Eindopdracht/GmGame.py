import random, sys, pygame, time, math, copy
import numpy as np
from pygame.locals import KEYUP, QUIT, MOUSEBUTTONUP, K_ESCAPE
from gomoku import Board, Move, GameState, valid_moves, pretty_board
from GmUtils import GmUtils
from GmGameRules import GmGameRules
from basePlayer import basePlayer

# The Gomoku Game class (visualisation of the gameboard, allowing two agents to play against eachother)
class GmGame:
    DIFFICULTY = 1  # how many moves to look ahead. (>2 is usually too much)

    SPACESIZE = 35  # size of the tokens and individual board spaces in pixels

    FPS = 30  # frames per second to update the screen
    WINDOWWIDTH = 1024  # width of the program's window, in pixels
    WINDOWHEIGHT = 768  # height in pixels

    XMARGIN = 0  # will be calculated at call of start()
    YMARGIN = 0

    BRIGHTBLUE = (0, 50, 255)
    LIGHTGRAY = (155, 150, 140)
    WHITE = (255, 255, 255)

    BGCOLOR = LIGHTGRAY
    TEXTCOLOR = WHITE

    BLACK = 1
    WHITE = 2
    EMPTY = 0
    MARKER = 3  # cannot be on board, but can be displayed
    HUMAN = "human"  # WHITE player
    HUMAN2 = "human2"  # BLACK player
    COMPUTER = "computer"  # BLACK player

    BlackPlayer = ""
    WhitePlayer = ""

    GameType_HumanVsCpu = "HumanVsCpu"
    GameType_HumanVsHuman = "HumanVsHuman"

    FPSCLOCK = None

    # if you want to test an ai game maximally quickly, you could disable showIntermediateMoves
    # player1 will be set to black.
    # player2 wil be set to white
    def start(player1, player2, max_time_to_move, showIntermediateMoves=True):
        GmGame.XMARGIN = int(
            (GmGame.WINDOWWIDTH - GmGameRules.BOARDWIDTH * GmGame.SPACESIZE) / 2
        )
        GmGame.YMARGIN = int(
            (GmGame.WINDOWHEIGHT - GmGameRules.BOARDHEIGHT * GmGame.SPACESIZE) / 2
        )

        global FPSCLOCK, DISPLAYSURF, WHITETOKENIMG
        global BLACKTOKENIMG, BOARDIMG, ARROWIMG, ARROWRECT, HUMANWINNERIMG
        global COMPUTERWINNERIMG, WINNERRECT, TIEWINNERIMG, MARKERIMG

        pygame.init()
        GmGame.FPSCLOCK = pygame.time.Clock()
        DISPLAYSURF = pygame.display.set_mode((GmGame.WINDOWWIDTH, GmGame.WINDOWHEIGHT))
        pygame.display.set_caption("Gomoku")

        WHITETOKENIMG = pygame.image.load(
            "assets/5row_white_smaller.png"
        ).convert_alpha()
        WHITETOKENIMG = pygame.transform.smoothscale(
            WHITETOKENIMG, (GmGame.SPACESIZE, GmGame.SPACESIZE)
        )
        BLACKTOKENIMG = pygame.image.load(
            "assets/5row_black_smaller.png"
        ).convert_alpha()
        BLACKTOKENIMG = pygame.transform.smoothscale(
            BLACKTOKENIMG, (GmGame.SPACESIZE, GmGame.SPACESIZE)
        )
        MARKERIMG = pygame.image.load("assets/marker.png").convert_alpha()
        MARKERIMG = pygame.transform.smoothscale(
            MARKERIMG, (GmGame.SPACESIZE, GmGame.SPACESIZE)
        )
        BOARDIMG = pygame.image.load("assets/gomoku_board.png").convert_alpha()
        BOARDIMG = pygame.transform.smoothscale(
            BOARDIMG, (GmGame.SPACESIZE, GmGame.SPACESIZE)
        )

        HUMANWINNERIMG = pygame.image.load(
            "assets/5row_blackwinner.png"
        ).convert_alpha()
        COMPUTERWINNERIMG = pygame.image.load(
            "assets/5row_whitewinner.png"
        ).convert_alpha()
        # make the winner impage small, such that we can cramp it in the topleft
        HUMANWINNERIMG = pygame.transform.smoothscale(
            HUMANWINNERIMG, (5 * GmGame.SPACESIZE, 2 * GmGame.SPACESIZE)
        )
        COMPUTERWINNERIMG = pygame.transform.smoothscale(
            COMPUTERWINNERIMG, (5 * GmGame.SPACESIZE, 2 * GmGame.SPACESIZE)
        )
        TIEWINNERIMG = pygame.image.load("assets/5row_tie.png").convert_alpha()
        WINNERRECT = HUMANWINNERIMG.get_rect()
        # WINNERRECT.center = (int(WINDOWWIDTH / 2), int(WINDOWHEIGHT / 2))
        WINNERRECT.left = 0
        WINNERRECT.top = 0

        while True:
            player1.new_game(
                True
            )  # to avoid inconsistencies, I define player1 as black player and player 2 as white player.
            player2.new_game(False)
            GmGame.runGame(player1, player2, max_time_to_move, showIntermediateMoves)

    def runGame(
        player1,
        player2,
        max_time_to_move,
        showIntermediateMoves,
    ):
        last_move = ()  # was None, changed for compatibility with competition.py
        ply = 1

        # black goes first
        activePlayer = player1 if player1.black else player2

        # Set up a blank board data structure.
        mainBoard = GmGame.getNewBoard()

        while True:  # main game loop
            # I don't bother to fill valid_moves. My class bookkeeps that by itself.
            gamestate = (mainBoard, ply)
            last_move = (column, row) = activePlayer.move(
                gamestate, last_move, max_time_to_move
            )
            ply += 1

            color = GmGame.getPlayerColor(activePlayer)

            if GmUtils.isValidMove(mainBoard, column, row):
                GmUtils.addMoveToBoard(mainBoard, last_move, color)
                if showIntermediateMoves:
                    GmGame.drawBoardWithExtraTokens(
                        mainBoard, column, row, GmGame.MARKER
                    )

            if GmUtils.isWinningMove(last_move, mainBoard):
                if activePlayer == player1:
                    winnerImg = HUMANWINNERIMG
                else:
                    winnerImg = COMPUTERWINNERIMG
                break
            elif GmGame.isBoardFull(mainBoard):
                # A completely filled board means it's a tie.
                winnerImg = TIEWINNERIMG
                if showIntermediateMoves:
                    GmGame.drawBoardWithExtraTokens(
                        mainBoard, last_move[0], last_move[1], GmGame.MARKER
                    )
                break
            activePlayer = GmUtils.getNonActivePlayer(activePlayer, player1, player2)

            if showIntermediateMoves:
                pygame.display.update()
                GmGame.FPSCLOCK.tick()

        while True:
            # Keep looping until player clicks the mouse or quits.
            GmGame.drawBoardWithExtraTokens(
                mainBoard, last_move[0], last_move[1], GmGame.MARKER
            )
            DISPLAYSURF.blit(winnerImg, WINNERRECT)
            pygame.display.update()
            GmGame.FPSCLOCK.tick()

            for event in pygame.event.get():  # event handling loop
                if event.type == QUIT or (
                    event.type == KEYUP and event.key == K_ESCAPE
                ):
                    pygame.quit()
                    sys.exit()
                elif event.type == MOUSEBUTTONUP:
                    return

    # token can be BLACK, WHITE or MARKER
    def drawToken(token, row, col):
        if token != None:
            spaceRect = pygame.Rect(0, 0, GmGame.SPACESIZE, GmGame.SPACESIZE)
            spaceRect.topleft = (
                GmGame.XMARGIN + (col * GmGame.SPACESIZE),
                GmGame.YMARGIN + (row * GmGame.SPACESIZE),
            )
            if token == GmGame.WHITE:
                DISPLAYSURF.blit(WHITETOKENIMG, spaceRect)
            elif token == GmGame.BLACK:
                DISPLAYSURF.blit(BLACKTOKENIMG, spaceRect)
            elif token == GmGame.MARKER:
                DISPLAYSURF.blit(MARKERIMG, spaceRect)

    def drawBoard(board, extraToken=None):
        DISPLAYSURF.fill(GmGame.BGCOLOR)

        spaceRect = pygame.Rect(0, 0, GmGame.SPACESIZE, GmGame.SPACESIZE)

        # draw board under the tokens
        for row in range(GmGameRules.BOARDHEIGHT):
            for col in range(GmGameRules.BOARDWIDTH):
                spaceRect.topleft = (
                    GmGame.XMARGIN + (col * GmGame.SPACESIZE),
                    GmGame.YMARGIN + (row * GmGame.SPACESIZE),
                )
                DISPLAYSURF.blit(BOARDIMG, spaceRect)

        # draw tokens
        for row in range(GmGameRules.BOARDHEIGHT):
            for col in range(GmGameRules.BOARDWIDTH):
                spaceRect.topleft = (
                    GmGame.XMARGIN + (col * GmGame.SPACESIZE),
                    GmGame.YMARGIN + (row * GmGame.SPACESIZE),
                )
                if board[row][col] == GmGame.WHITE:
                    DISPLAYSURF.blit(WHITETOKENIMG, spaceRect)
                elif board[row][col] == GmGame.BLACK:
                    DISPLAYSURF.blit(BLACKTOKENIMG, spaceRect)

        # draw the extra token
        if extraToken != None:
            GmGame.drawToken(extraToken)

    def drawBoardWithExtraTokens(board, row=0, col=0, token1=None, token2=None):
        GmGame.drawBoard(board)
        if token1 != None:
            GmGame.drawToken(token1, row, -1)
            GmGame.drawToken(token1, -1, col)

        if token2 != None:
            GmGame.drawToken(token2, row, -1)
            GmGame.drawToken(token2, -1, col)

    def getNewBoard():
        return np.zeros(
            (GmGameRules.BOARDWIDTH, GmGameRules.BOARDHEIGHT), dtype=np.int8
        )

    def isBoardFull(board):
        # Returns True if there are no empty spaces anywhere on the board.
        for row in range(GmGameRules.BOARDHEIGHT):
            for col in range(GmGameRules.BOARDWIDTH):
                if board[row][col] == GmGame.EMPTY:
                    return False
        return True

    def getPlayerColor(player_):
        return GmGame.BLACK if player_.black else GmGame.WHITE
