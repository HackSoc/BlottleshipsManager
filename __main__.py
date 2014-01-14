import argparse
from battleships_gui import BattleshipsGraphics
import const
import Players
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
            gui.drawPlayer(firstPlayer.name,
                           firstPlayer.description, 'left')
            gui.drawPlayer(secondPlayer.name,
                           secondPlayer.description, 'right')
            gui.drawScore(scorePlayer1, scorePlayer2)

        turn = (-1)**game

        if playGame(firstPlayer, secondPlayer, turn, gui) == firstPlayer:
            scorePlayer1 += 1
        else:
            scorePlayer2 += 1

        print "---------------- ", firstPlayer.name, scorePlayer1, "-",
        print scorePlayer2, secondPlayer.name, "----------------"

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


def playGame(firstPlayer, secondPlayer, turn, gui):
    # Distribute the fleet onto each player board
    firstPlayer.deployFleet()
    secondPlayer.deployFleet()

    if gui:
        for row in range(len(firstPlayer.board)):
            for col in range(len(firstPlayer.board[row])):
                if firstPlayer.board[row][col] == const.OCCUPIED:
                    gui.drawBoat('left', row, col)

        for row in range(len(secondPlayer.board)):
            for col in range(len(secondPlayer.board[row])):
                if secondPlayer.board[row][col] == const.OCCUPIED:
                    gui.drawBoat('right', row, col)

    while True:
        a = firstPlayer if turn > 0 else secondPlayer
        b = secondPlayer if turn > 0 else firstPlayer

        # Make a move by looking at the opponent's board
        try:
            with Watchdog(watchdog_time):
                row, col = a.chooseMove()
        except Watchdog:
            print "Player {} took longer than {}s for chooseMove".format(
                "1" if turn > 0 else "2",
                watchdog_time)
            return b

        # Ask the user to enter the outcome
        outcome = giveOutcome(b.board, row, col)

        if gui:
            if outcome == const.HIT:
                gui.drawHit('right' if turn > 0 else 'left', row, col)
            else:
                gui.drawMiss('right' if turn > 0 else 'left', row, col)

        try:
            with Watchdog(watchdog_time):
                a.setOutcome(outcome, row, col)
        except Watchdog:
            print "Player {} took longer than {}s for setOutcome".format(
                "1" if turn > 0 else "2",
                watchdog_time)
            return b

        try:
            with Watchdog(watchdog_time):
                b.getOpponentMove(row, col)
        except Watchdog:
            print "Player {} took longer than {}s for getOpponentMove".format(
                "2" if turn > 0 else "1",
                watchdog_time)
            return a

        if checkWinner(b.board):
            return a

        turn *= -1

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
        name = listPlayers[player[3]].name

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
parser.add_argument("-g", "--gui", action="store_true",
                    help="Run with a GUI (default: %(default)s)")
parser.add_argument("--rounds", default=10, type=int,
                    help="""Number of rounds to run per
                            game (default: %(default)s)""")

args = parser.parse_args()

# Import players files
playerList = Players.load()

guiInstance = None
if args.gui:
    guiInstance = BattleshipsGraphics(12)  # Gridsize of 12

resultsTable = playChampionship(playerList, args.rounds, guiInstance)
printTable(resultsTable, playerList)

if args.gui:
    # Must be the last line of code
    guiInstance.screen.exitonclick()
