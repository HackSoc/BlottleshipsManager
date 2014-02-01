#!/usr/bin/env python2

import argparse
import const
import playerloader
from watchdog import Watchdog

##########################################
##              PARAMETERS              ##
##########################################

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

def initialiseChampionshipTable(listPlayers):
    table = {}
    for playerNumber in range(len(listPlayers)):
        playerStats = {}
        playerStats["Win"] = 0
        playerStats["Draw"] = 0
        playerStats["Loss"] = 0
        playerStats["For"] = 0
        playerStats["Against"] = 0
        table[playerNumber] = playerStats

    return table


def playChampionship(listPlayers, rounds, gui):
    table = initialiseChampionshipTable(listPlayers)
    totalPlayers = len(listPlayers)
    listGames = []
    for home in range(totalPlayers - 1):
        for away in range(home + 1, totalPlayers):
            listGames.append((home, away))

    print listGames
    for game in listGames:
        result = playMatch(listPlayers[game[0]],
                           listPlayers[game[1]], rounds, gui)
        firstPlayerStats = table[game[0]]
        secondPlayerStats = table[game[1]]

        # Draw
        if result[0] == result[1]:
            firstPlayerStats["Draw"] += 1
            secondPlayerStats["Draw"] += 1

        # Player 1 win
        elif result[0] > result[1]:
            firstPlayerStats["Win"] += 1
            secondPlayerStats["Loss"] += 1

        # Player 2 win
        else:
            firstPlayerStats["Loss"] += 1
            secondPlayerStats["Win"] += 1

        firstPlayerStats["For"] += result[0]
        firstPlayerStats["Against"] += result[1]
        secondPlayerStats["For"] += result[1]
        secondPlayerStats["Against"] += result[0]

    return table


def playMatch(firstPlayer, secondPlayer, rounds, gui):
    scorePlayer1 = scorePlayer2 = 0
    for game in range(rounds):
        if gui:
            gui.turtle.clear()
            gui.drawBoards()
            gui.drawPlayer(firstPlayer.getName(),
                           firstPlayer.getDescription(), 'left')
            gui.drawPlayer(secondPlayer.getName(),
                           secondPlayer.getDescription(), 'right')
            gui.drawScore(scorePlayer1, scorePlayer2)

        turn = (-1)**game
        winner = playGame(firstPlayer, secondPlayer, turn, gui)

        if winner is firstPlayer:
            scorePlayer1 += 1
        else:
            scorePlayer2 += 1

        print "---------------- ", firstPlayer.getName(), scorePlayer1, "-",
        print scorePlayer2, secondPlayer.getName(), "----------------"

        if gui:
            gui.drawScore(scorePlayer1, scorePlayer2)

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
    except Watchdog, e:
        print "{} took longer longer than {}s for {}()"\
            .format(player.getName(), watchdog_time, action.__name__)
        raise


def playGame(firstPlayer, secondPlayer, turn, gui):

    # Distribute the fleet onto each player board
    try:
        firstPlayer._playerBoard = timedAction(firstPlayer, firstPlayer.deployFleet)
    except Watchdog:
        return secondPlayer
    try:
        secondPlayer._playerBoard = timedAction(secondPlayer, secondPlayer.deployFleet)
    except Watchdog:
        return firstPlayer

    if gui:
        for row in range(len(player1_board)):
            for col in range(len(player1_board[row])):
                if firstPlayer._playerBoard[row][col] == const.OCCUPIED:
                    gui.drawBoat('right', row, col)

        for row in range(len(player2_board)):
            for col in range(len(player2_board[row])):
                if secondPlayer._playerBoard[row][col] == const.OCCUPIED:
                    gui.drawBoat('left', row, col)

    haveWinner = False
    player1Moves = 0
    player2Moves = 0
    while not haveWinner:
        if turn > 0:
            # Make a move by looking at the opponent's board
            try:
                i1, i2 = timedAction(firstPlayer, firstPlayer.chooseMove)
            except Watchdog:
                return secondPlayer

            # Get result of move
            outcome = giveOutcome(secondPlayer._playerBoard, i1, i2)

            if gui:
                if outcome == const.HIT:
                    gui.drawHit('left', i1, i2)
                else:
                    gui.drawMiss('left', i1, i2)

            try:
                timedAction(firstPlayer, firstPlayer.setOutcome, outcome, i1, i2)
            except Watchdog:
                return secondPlayer

            try:
                timedAction(secondPlayer, secondPlayer.getOpponentMove, i1, i2)
            except Watchdog:
                return firstPlayer

            # Show the current board state
            haveWinner = checkWinner(secondPlayer._playerBoard)
            player1Moves += 1

        else:
            # Make a move by looking at the opponent's board
            try:
                i1, i2 = timedAction(secondPlayer, secondPlayer.chooseMove)
            except Watchdog:
                return firstPlayer

            # Get result of move
            outcome = giveOutcome(firstPlayer._playerBoard, i1, i2)

            if gui:
                if outcome == const.HIT:
                    gui.drawHit('right', i1, i2)
                else:
                    gui.drawMiss('right', i1, i2)

            try:
                timedAction(secondPlayer, secondPlayer.setOutcome, outcome, i1, i2)
            except Watchdog:
                return firstPlayer

            try:
                timedAction(firstPlayer, firstPlayer.getOpponentMove, i1, i2)
            except Watchdog:
                return secondPlayer

            # Show the current board state
            haveWinner = checkWinner(firstPlayer._playerBoard)
            player2Moves += 1
        turn *= -1

    if args.verbose:
        print "Player1 moves: {}; Player2 moves: {}".format(player1Moves,
                                                            player2Moves)
    return secondPlayer if turn > 0 else firstPlayer


def printTable(table, listPlayers):
    wins = 3
    draws = 1
    losses = 0
    listResults = []
    for player in table:
        stats = table[player]
        points = wins * stats["Win"]\
            + draws * stats["Draw"]\
            + losses * stats["Loss"]
        setsFor = stats["For"]
        setsAgainst = stats["Against"]
        listResults.append((points, setsFor - setsAgainst, setsFor, player))

    listResults.sort(reverse=True)
    pos = 1
    print " | pos | ", "   Name                ", " | ", " W ", " D ", " L ",
    print "  F ", "  ", " | ", "Points |"
    for player in listResults:
        name = listPlayers[player[3]].getName()

        # Padding name
        if len(name) <= 25:
            name += ' ' * (25 - len(name))
        else:
            name = name[:25]

        stats = table[player[3]]
        print ' | {:3} | {} | {:3} {:3} {:3} {:4} {:4} | {:5}   |'\
            .format(pos, name, stats["Win"], stats["Draw"], stats["Loss"],
                    stats["For"], stats["Against"], player[0])

        pos += 1

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

resultsTable = playChampionship(playerList, args.rounds, guiInstance)
printTable(resultsTable, playerList)

if args.gui:
    # Must be the last line of code
    guiInstance.screen.exitonclick()
