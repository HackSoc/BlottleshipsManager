#!/usr/bin/env python2

import argparse
import const
import playerloader
from watchdog import Watchdog

# PARAMETERS

watchdog_time = 2  # How many seconds to allow AIs for each function call.


# Check whether the fleet is sunk
def checkWinner(board):
    # We just need to test whether the number of hits
    # equals the total number of squares in the fleet
    hits = 0
    for i in range(12):
        hits += board[i].count(const.HIT)
    return hits == 21


def giveOutcome(player_board, i1, i2):
    if (player_board[i1][i2] == const.OCCUPIED
            or player_board[i1][i2] == const.HIT):
        # They may (stupidly) hit the same square
        # twice so we check for occupied or hit
        player_board[i1][i2] = const.HIT
        return const.HIT
    else:
        # You might like to keep track of where your opponent
        # has missed, but here we just acknowledge it
        return const.MISSED


def playChampionship(listPlayers, rounds, gui):
    # Make sure stats are at 0
    for playerwrap in listPlayers:
        playerwrap.reset_stats()

    totalPlayers = len(listPlayers)
    listGames = []
    for home in range(totalPlayers - 1):
        for away in range(home + 1, totalPlayers):
            listGames.append((home, away))

    print listGames
    for game in listGames:
        player1 = listPlayers[game[0]]
        player2 = listPlayers[game[1]]
        result = playMatch(player1, player2, rounds, gui)

        # Draw
        if result[0] == result[1]:
            player1.stats["Draw"] += 1
            player2.stats["Draw"] += 1

        # Player 1 win
        elif result[0] > result[1]:
            player1.stats["Win"] += 1
            player2.stats["Loss"] += 1

        # Player 2 win
        else:
            player1.stats["Loss"] += 1
            player2.stats["Win"] += 1

        player1.stats["For"] += result[0]
        player1.stats["Against"] += result[1]
        player2.stats["For"] += result[1]
        player2.stats["Against"] += result[0]


def printMatchRes(player1wrap, scorePlayer1, player2wrap, scorePlayer2):
    middle = str(scorePlayer1).zfill(2) + " - " + str(scorePlayer2).zfill(2)
    print ""
    print "----Rounds won---- ", player1wrap.ai.getName(),
    print middle,
    print player2wrap.ai.getName(), "----------------"

    print "-shots per Round-- ", player1wrap.ai.getName(),
    if scorePlayer1 == 0:
        print "NA",
    else:
        print str(player1wrap.stats["Moves"] / scorePlayer1).zfill(2),

    print "-",

    if scorePlayer2 == 0:
        print "NA",
    else:
        print str(player2wrap.stats["Moves"] / scorePlayer2).zfill(2),

    print player2wrap.ai.getName(), "----------------"
    print ""


def playMatch(player1wrap, player2wrap, rounds, gui):
    scorePlayer1 = scorePlayer2 = 0
    player1wrap.stats["Moves"] = 0
    player2wrap.stats["Moves"] = 0

    player1wrap.ai.newPlayer(player2wrap.ai.getName())
    player2wrap.ai.newPlayer(player1wrap.ai.getName())

    for game in range(rounds):
        player1wrap.ai.newRound()
        player2wrap.ai.newRound()

        if gui:
            gui.turtle.clear()
            gui.drawBoards()
            gui.drawPlayer(player1wrap.ai.getName(),
                           player1wrap.ai.getDescription(), 'left')
            gui.drawPlayer(player2wrap.ai.getName(),
                           player2wrap.ai.getDescription(), 'right')
            gui.drawScore(scorePlayer1, scorePlayer2)

        turn = (-1)**game
        winner = playGame(player1wrap, player2wrap, turn, gui)

        if winner is player1wrap.ai:
            scorePlayer1 += 1
        else:
            scorePlayer2 += 1

        if gui:
            gui.drawScore(scorePlayer1, scorePlayer2)

    printMatchRes(player1wrap, scorePlayer1, player2wrap, scorePlayer2)

    if gui:
        if scorePlayer2 > scorePlayer1:
            gui.drawWinner('right')
        elif scorePlayer2 == scorePlayer1:
            pass
        else:
            gui.drawWinner('left')

    return (scorePlayer1, scorePlayer2)


def timedAction(player, action, *args, **kwargs):
    try:
        with Watchdog(watchdog_time):
            return action(*args, **kwargs)
    except Watchdog:
        print "{} took longer longer than {}s for {}()"\
            .format(player.getName(), watchdog_time, action.__name__)
        raise


def playGame(player1wrap, player2wrap, turn, gui):

    # Distribute the fleet onto each player board
    try:
        player1wrap.ai._playerBoard = timedAction(player1wrap.ai,
                                                  player1wrap.ai.deployFleet)
    except Watchdog:
        return player2wrap
    try:
        player2wrap.ai._playerBoard = timedAction(player2wrap.ai,
                                                  player2wrap.ai.deployFleet)
    except Watchdog:
        return player1wrap

    if gui:
        for row in range(len(player1wrap.ai._playerBoard)):
            for col in range(len(player1wrap.ai._playerBoard[row])):
                if player1wrap.ai._playerBoard[row][col] == const.OCCUPIED:
                    gui.drawBoat('right', row, col)

        for row in range(len(player2wrap.ai._playerBoard)):
            for col in range(len(player2wrap.ai._playerBoard[row])):
                if player2wrap.ai._playerBoard[row][col] == const.OCCUPIED:
                    gui.drawBoat('left', row, col)

    player1Moves = 0
    player2Moves = 0
    while True:
        active = player1wrap.ai if turn > 0 else player2wrap.ai
        passive = player2wrap.ai if turn > 0 else player1wrap.ai

        # Make a move by looking at the opponent's board
        try:
            i1, i2 = timedAction(active, active.chooseMove)
        except Watchdog:
            return passive

        # Get result of move
        outcome = giveOutcome(passive._playerBoard, i1, i2)

        if gui:
            if outcome == const.HIT:
                gui.drawHit('left' if turn > 0 else 'right', i1, i2)
            else:
                gui.drawMiss('left' if turn > 0 else 'right', i1, i2)

        try:
            timedAction(active, active.setOutcome, outcome, i1, i2)
        except Watchdog:
            return passive

        try:
            timedAction(passive, passive.getOpponentMove, i1, i2)
        except Watchdog:
            return active

        if turn > 0:
            player1Moves += 1
        else:
            player2Moves += 1

        if checkWinner(passive._playerBoard):
            if args.verbose:
                print "Player1 moves: {}; Player2 moves: {}"\
                    .format(player1Moves, player2Moves)
            if turn > 0:
                player1wrap.stats["Moves"] += player1Moves
            else:
                player2wrap.stats["Moves"] += player2Moves
            return active

        turn *= -1


def printTable(listPlayers):
    listResults = []
    for player in listPlayers:
        setsFor = player.stats["For"]
        setsAgainst = player.stats["Against"]
        listResults.append((player.score(),
                            setsFor - setsAgainst,
                            setsFor, player))

    listResults.sort(reverse=True)
    pos = 1
    print " | pos | ", "   Name                ", " | ", " W ", " D ", " L ",
    print "  F ", "  A", "| ", "Points |"
    for res in listResults:
        name = res[3].ai.getName()

        # Padding name
        if len(name) <= 25:
            name += ' ' * (25 - len(name))
        else:
            name = name[:25]

        stats = res[3].stats
        print ' | {:3} | {} | {:3} {:3} {:3} {:4} {:4} | {:5}   |'\
            .format(pos, name, stats["Win"], stats["Draw"], stats["Loss"],
                    stats["For"], stats["Against"], res[0])

        pos += 1


# Start
parser = argparse.ArgumentParser(description="Blottleships Game Manager")
parser.add_argument("-v", "--verbose", action="store_true",
                    help="""Run with verbose console output
                            (default: %(default)s)""")
parser.add_argument("-g", "--gui", action="store_true",
                    help="Run with a GUI (default: %(default)s)")
parser.add_argument("--rounds", default=10, type=int,
                    help="""Number of rounds to run per
                            game (default: %(default)s)""")

args = parser.parse_args()

# Import players file
playerList = playerloader.import_players()

guiInstance = None
if args.gui:
    from battleships_gui import BattleshipsGraphics
    guiInstance = BattleshipsGraphics(12)  # Gridsize of 12

playChampionship(playerList, args.rounds, guiInstance)
printTable(playerList)

if args.gui:
    # Must be the last line of code
    guiInstance.screen.exitonclick()
