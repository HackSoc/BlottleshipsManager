##import os # Required for clear screen
from random import randint
import const
from battleships_gui import BattleshipsGraphics
import playerloader
from watchdog import Watchdog

# How many seconds to allow AIs for each function call.
watchdog_time = 2

## importing players file
listPlayers = playerloader.import_players()




# Check whether the fleet is sunk
def checkWinner(board):
    # We just need to test whether the number of hits equals the total number of squares in the fleet
    hits = 0
    for i in range(12):
        hits += board[i].count(4)
    return hits==21

def giveOutcome(player_board, i1, i2):
    if ((player_board[i1][i2]==const.OCCUPIED)
        or (player_board[i1][i2]==const.HIT)):
        # They may (stupidly) hit the same square twice so we check for occupied or hit
        player_board[i1][i2]=const.HIT
        result =const.HIT
    else:
        # You might like to keep track of where your opponent has missed, but here we just acknowledge it
        result = const.MISSED
    return result

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

def playChampionship(listPlayers, rounds, gui = None):
    table = initialiseChampionshipTable(listPlayers)
    totalPlayers = len(listPlayers)
    listGames = []
    for home in range(totalPlayers - 1):
        for away in range(home+1, totalPlayers):
            listGames.append((home, away))

    print listGames
    for game in listGames:
        result = playMatch(listPlayers[game[0]], listPlayers[game[1]], rounds, gui)
        firstPlayerStats = table[game[0]]
        secondPlayerStats = table[game[1]]
        if result[0] == result[1]: ##Draw
            firstPlayerStats["Draw"] += 1
            firstPlayerStats["For"] += result[0]
            firstPlayerStats["Against"] += result[1]
            secondPlayerStats["Draw"] += 1
            secondPlayerStats["For"] += result[1]
            secondPlayerStats["Against"] += result[0]

        elif result[0] > result[1]: ##Player 1 win
            firstPlayerStats["Win"] += 1
            firstPlayerStats["For"] += result[0]
            firstPlayerStats["Against"] += result[1]
            secondPlayerStats["Loss"] += 1
            secondPlayerStats["For"] += result[1]
            secondPlayerStats["Against"] += result[0]

        else:##Player 2 win
            firstPlayerStats["Loss"] += 1
            firstPlayerStats["For"] += result[0]
            firstPlayerStats["Against"] += result[1]
            secondPlayerStats["Win"] += 1
            secondPlayerStats["For"] += result[1]
            secondPlayerStats["Against"] += result[0]

##        raw_input("press enter!")

    return table


def playMatch(firstPlayer, secondPlayer, rounds, gui = None):
    scorePlayer1 = scorePlayer2 = 0
    for game in range(rounds):
        if gui:
            gui.turtle.clear()
            gui.drawBoards()
            gui.drawPlayer(firstPlayer.getName(), firstPlayer.getDescription(), 'left')
            gui.drawPlayer(secondPlayer.getName(), secondPlayer.getDescription(), 'right')
            gui.drawScore (scorePlayer1, scorePlayer2)

        turn = (-1)**game
        p1, p2 = playGame(firstPlayer, secondPlayer, turn, gui)

        scorePlayer1 += p1
        scorePlayer2 += p2

        print "---------------- ",firstPlayer.getName(), scorePlayer1,"-",
        print scorePlayer2, secondPlayer.getName(), "----------------"

        if gui:
            gui.drawScore (scorePlayer1, scorePlayer2)

    if gui:
        if scorePlayer2 > scorePlayer1 :
            gui.drawWinner('right')
        elif scorePlayer2 == scorePlayer1:
            pass
        else:
            gui.drawWinner('left')


    return (scorePlayer1, scorePlayer2)



def playGame(firstPlayer, secondPlayer, turn, gui = None):
    # Distribute the fleet onto each player board
    player1_board = firstPlayer.deployFleet()

    for row in range(len(player1_board)):
        for col in range(len(player1_board[row])):
            if gui and player1_board[row][col] == const.OCCUPIED:
                gui.drawBoat('right', row, col)

    player2_board = secondPlayer.deployFleet()
    for row in range(len(player2_board)):
        for col in range(len(player2_board[row])):
            if gui and player2_board[row][col] == const.OCCUPIED:
                gui.drawBoat('left', row, col)

##    raw_input("press enter!")

    haveWinner = False
    while not haveWinner:
        if turn > 0:
            # Make a move by looking at the opponent's board
            try:
              with Watchdog(watchdog_time):
                i1,i2 = firstPlayer.chooseMove()
            except Watchdog:
              print "Player 1 took longer than 2s for Player.chooseMove()."
              return (0, 1)

            # Ask the user to enter the outcome
            outcome = giveOutcome(player2_board, i1, i2)
##            print "outcome of", chr(i1+65), i2+1, "is:", outcome

            if gui:
                if outcome == const.HIT:
                    gui.drawHit('left', i1, i2)
                else:
                    gui.drawMiss('left', i1, i2)

            try:
              with Watchdog(watchdog_time):
                firstPlayer.setOutcome(outcome, i1, i2)
            except Watchdog:
              print "Player 1 took longer than 2s for Player.setOutcome()."
              return (0, 1)

            try:
              with Watchdog(watchdog_time):
                secondPlayer.getOpponentMove(i1, i2)
            except Watchdog:
              print "Player 2 took longer than 2s for Player.getOpponentMove()."
              return (1, 0)

            # Show the current board state
            turn *= -1
            haveWinner = checkWinner(player2_board)

        else:
            # Make a move by looking at the opponent's board
            try:
              with Watchdog(watchdog_time):
                i1,i2 = secondPlayer.chooseMove()
            except Watchdog:
              print "Player 2 took longer than 2s for Player.chooseMove()."
              return (1, 0)

            # Ask the user to enter the outcome
            outcome = giveOutcome(player1_board, i1, i2)
##            print "outcome of", chr(i1+65), i2+1, "is:", outcome
            if gui:
                if outcome == const.HIT:
                    gui.drawHit('right', i1, i2)
                else:
                    gui.drawMiss('right', i1, i2)

            try:
              with Watchdog(watchdog_time):
                secondPlayer.setOutcome(outcome, i1, i2)
            except Watchdog:
              print "Player 2 took longer than 2s for Player.setOutcome()."
              return (1, 0)

            try:
              with Watchdog(watchdog_time):
                firstPlayer.getOpponentMove(i1, i2)
            except Watchdog:
              print "Player 1 took longer than 2s for Player.getOpponentMove()."
              return (0, 1)

            # Show the current board state
            turn *= -1
            haveWinner = checkWinner(player1_board)

    winner = "Player 1"
    if turn > 0 :
        winner = "Player 2"
        result = (0,1)
    else:
        result = (1,0)


    return result

def printTable(table, listPlayers):
    wins = 3
    draws = 1
    losses = 0
    listResults = []
    for player in table:
        stats = table[player]
        points = wins * stats["Win"] + draws * stats["Draw"] + losses * stats["Loss"]
        setsFor = stats["For"]
        setsAgainst = stats["Against"]
        listResults.append((points, setsFor - setsAgainst, setsFor, player))

    listResults.sort(reverse = True)
    pos = 1
    print " | pos | ", "   Name                ", " | ", " W ", " D ", " L ",
    print "  F ", "  ", " | ", "Points |"
    for player in listResults:
        name = listPlayers[player[3]].getName()

        if len(name)<= 25: ## padding name
            name += ' ' * (25-len(name))
        else:
            name = name[:25]

        stats = table[player[3]]
        print ' | {:3} | {} | {:3} {:3} {:3} {:4} {:4} | {:5}   |'.format(pos,name,stats["Win"],stats["Draw"],
                                                                          stats["Loss"], stats["For"],
                                                                          stats["Against"], player[0])

        pos += 1


# Main
##gui = BattleshipsGraphics(12)
table = playChampionship(listPlayers, 49000)
printTable(table, listPlayers)







## Must be the last line of code
##gui.screen.exitonclick()

