#!/usr/bin/env python3

# Gomoku Test Environment versie 1.6
# (by Marius Versteegen)

# FIRST, RUN THIS AT THE ANACONDA PROMPT (to download the pygame library)
# python -m pip install -U pygame --user
# or, in pycharm, click on the "Terminal" tab at the bottom to open a terminal.
# in the terminal, you can type the same as above to install the pygame libary.

# Let op!  Als je de game runt, lijkt er niets te gebeurren.
# De game start immers geminimaliseerd op, en zal knipperen op je task-bar.
# Klik op de game icon in de task-bar (een bijtje) om de game te maximaliseren.

# Tips + potentiele instinkers bij Gomoku
"""
    Deze voorbeeldcode heeft een aantal handige test-faciliteiten:
    - Via een gui kun je zelf meespelen, als je een (of meerdere) human player toevoegt (via GmGame).

    - Er zit ook een test bij (GmQuickTests), waarmee je je AI kunt testen. Het is handig
      om te beginnen bij de bovenste test (en de overige tests uit te commentarieren).
      Blijf debuggen totdat de test slaagt en dan verder.
      Je zult zien dat als je AI slaagt voor de tests, dat hij het dan ook heel goed doet
      als je er als mens tegen speelt via

    * Begin met het implementeren van de pseusdocode voor een zuivere MontecarloPlayer.
    * Test die met een klein board (7x7) om de basis-algoritmen te debuggen.
      Die size kun je instellen in gomoku.py
    * Gebruik de debugger, met breakpoints en de mogelijkheid om dingen tijdens zo'n breakpoint
        aan te roepen, zoals self.printTree(node)
    * Gebruik ook de profiler (in plaats van timeit) om een goed overzicht te krijgen van waar de
      rekentijd zit.

    FindSpotToExpand:
    * Let op: een winning node is meteen ook een terminal node!

    Rollout:
    * Als de startnode van een Rollout al winning is, heeft het geen zin
      om additionele rolls te doen.
    * Zorg ervoor dat je rollout niet je node verandert.
    * Een enkele deepcopy aan het begin van een Rollout volstaat. Maak dus niet na elke roll een deepcopy van je bord.
    * Ga niet na elke rollout de validmoves opnieuw laten uitrekenen. Haal de laatste move gewoon uit de lijst.
    * Ga niet binnen de rollout nodes toevoegen aan je tree
    * retourneer als resultaat van je rollout 1 (jouw AI wint), -1 (tegenstander wint) of 0

    BackupValue:
    * Zorg ervoor dat de Q van een node omhoog gaat als het resultaat voor jouw AI gunstig was.
      NB: jouw AI kan met zwart spelen, maar ook met wit.

    Main routine:
    * Roep na elke findspottoexpand rollout en backupvalue vaak genoeg aan. Bijvoorbeeld 10x.
    * Het kind met de beste zet heeft de hoogste Q/N, niet de hoogste UCT.

    Tips en Best practices:
    * Maak een printNode en printTree functie, waardoor je snel een overzicht kunt krijgen van
      een enkele node en haar kinderen of in het geval van printTree: de hele boom die er onder hangt.
      Print van elke node positie, N, Q en uct
    * Houd je Montecarlo-player klasse klein. Verhuis 2e orde utility functies naar een andere klasse
      met @staticmethod functies.
    * De beste move die je uiteindelijk selecteert is niet de move met de hoogste Q, maar de move met de hoogste Q/N
      (NB: de findspot to expand gebruikt daarentegen de uitkomst van de uct formule als criterium)
    * Je zult merken dat 5 op een rij op een 7x7 board met zuiver MontecarloPlayer als tegenstander heel goed
      kan werken.
    * Om de effectiviteit van je heuristiek te testen zou je voorlopig op dat bord kunnen blijven testen,
      en kijken of je dankzij die heuristiek je rekentijd met een bepaalde factor kunt verkleinen-zonder dat het
      tegenspel slecht wordt.
    * Je zou in het begin eventueel kunnen aanemen dat je AI altijd voor zwart speelt, en achteraf nog even
      aanpassingen maken waardoor het ook goed voor wit speelt.
    * Voor debuggability heb je reproduceerbaarheid nodig.
      Controleer daarom voor het debuggen of random.seed in deze file nog op 0 wordt gezet.
      Gebruik daarom tijdens het debuggen ook een vast aantal loops ipv te wachten op het verstrijken van een seconde.
      (als je op tijd wacht, is het aantal loops afhankelijk van de toevallige belasting van je processor
       door andere systeemtaken)
    * Als je wilt zoeken naar een tuple - wat heeft dan een gunstiger orde: een list of set of dict?
    * Besef je dat strings, ints, floats en bools altijd echt gekopieerd worden,
      en het overige by reference.
    * Verdiep je in copy.copy en copy.deepcopy en wees je bewust van het verschil.

    Essentiele dingen om je te realiseren tijdens het debuggen:
    * positie op bord met waarde 2 = zwarte steen
      positie op bord met waarde 1 = witte steen
      positie op bord met waarde 0 = lege plek
    * gomoku.prettyBoard(state) laat zien:
         O  voor zwarte steen
         X  voor witte steen
    * Een state met oneven ply betekent: zwart is aan zet (en een eventuele last_move is dus van wit)
    * Een hoge Q/N in een node betekent: die stelling is gunstig voor jouw AI

    v1.1 Het werkt nu ook als het boad een numpy array is.
    V1.2 Full fledged gomoku game rules.
    V1.3 Restrictions on second move lifted.
    v1.4 Gebruik overal (row,col) om moves te representeren. Geen (x,y) meer.
    v1.5 GmQuickTests toegevoegd.
    v1.6 GmGame retourneert nu het empty tuple () als initiele last_move (ipv None)
         - conform het gedrag van gomoku competition, checklist geupdate (correctie: zwart=2 en O).
    v1.61 GmQuickTest initialiseert player voor de test op de juiste kleur via new_game.
    v1.62 gomoku_ai_marius1_webclient werkte bij nieuwere python versies niet meer in competition.
          Dat is nu gefixed.
          Verder meer tests toegevoegd, ook tests waarbij je AI als wit speelt
    v1.63 gomoku_ai_marius1_webclient en random webclient werkten niet op kleinere
          borden in de competition. Dat is nu gefixed.
"""

# TODO: start with Move Center

import random, sys, pygame, time, math, copy
import numpy as np
from pygame.locals import KEYUP, QUIT, MOUSEBUTTONUP, K_ESCAPE
from gomoku import Board, Move, GameState, valid_moves, pretty_board
from GmUtils import GmUtils
from GmGameRules import GmGameRules
from gomoku_ai_marius1_webclient import gomoku_ai_marius1_webclient
from gomoku_ai_random_webclient import gomoku_ai_random_webclient
from basePlayer import basePlayer
from GmGame import GmGame
from GmQuickTests import GmQuickTests

# player gives an implementation the basePlayer cl
class randomPlayer(basePlayer):
    def __init__(self, black_=True):
        self.black = black_

        self.max_move_time_ns = 0
        self.start_time_ns = 0

    def new_game(self, black_: bool):
        """At the start of each new game you will be notified by the competition.
        this method has a boolean parameter that informs your agent whether you
        will play black or white.
        """
        self.black = black_

    def move(
        self, state: GameState, last_move: Move, max_time_to_move: int = 1000
    ) -> Move:
        board = state[0]
        ply = state[1]

        validMoves = GmUtils.getValidMoves(board, ply)

        return random.choice(validMoves)

    def id(self) -> str:
        """Please return a string here that uniquely identifies your submission e.g., "name (student_id)" """
        return "random_player"


class humanPlayer(basePlayer):
    def __init__(self, black_=True):
        self.black = black_

    def new_game(self, black_):
        self.black = black_

    def move(self, gamestate, last_move, max_time_to_move=1000):
        board = gamestate[0]
        tokenx, tokeny = None, None
        while True:
            for event in pygame.event.get():  # event handling loop
                if event.type == QUIT:
                    pygame.quit()
                    sys.exit()
                elif event.type == MOUSEBUTTONUP:
                    tokenx, tokeny = event.pos
                    if (
                        GmGame.YMARGIN < tokeny < GmGame.WINDOWHEIGHT - GmGame.YMARGIN
                        and GmGame.XMARGIN
                        < tokenx
                        < GmGame.WINDOWWIDTH - GmGame.XMARGIN
                    ):
                        # place it
                        col = int((tokenx - GmGame.XMARGIN) / GmGame.SPACESIZE)
                        row = int((tokeny - GmGame.YMARGIN) / GmGame.SPACESIZE)
                        # print("row:{},col:{}".format(row,column))
                        if GmUtils.isValidMove(board, row, col):
                            return (row, col)
                    tokenx, tokeny = None, None

            if last_move != None and last_move != ():
                GmGame.drawBoardWithExtraTokens(
                    board, last_move[0], last_move[1], GmGame.MARKER
                )
            else:
                GmGame.drawBoard(board)

            pygame.display.update()
            GmGame.FPSCLOCK.tick()

    def id(self):
        return "Marius"


random.seed(0)  # voor reproduceerbare debugging

humanPlayer1 = humanPlayer()
humanPlayer2 = humanPlayer()

aiPlayer1 = randomPlayer()
aiPlayer2 = gomoku_ai_marius1_webclient(
    True, GmGameRules.winningSeries, GmGameRules.BOARDWIDTH
)
aiPlayer3 = gomoku_ai_random_webclient(
    True, GmGameRules.winningSeries, GmGameRules.BOARDWIDTH
)

# uncomment the line below to test again yourself as human (player1 is black and starts the game)
GmGame.start(
    player1=aiPlayer2,
    player2=humanPlayer1,
    max_time_to_move=1000,
    showIntermediateMoves=True,
)  # don't speciry an aiPlayer for Human vs Human games

# uncomment the line below to run some simple tests for quick analysis and debugging.
# GmQuickTests.doAllTests(aiPlayer2)
