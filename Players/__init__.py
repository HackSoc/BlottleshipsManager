from random import randint
import const


class BasePlayer:
    def __init__(self):
        """
        Initialise the boards: player to empty, opponent to unknown.
        """
        self._playerName = "Unknown"
        self._playerDescription = "None"

    def getName(self):
        return self._playerName

    def getDescription(self):
        return self._playerDescription

    def _initBoards(self):
        """
        The boards are stored in a "jagged" 2 dimensional list
        Example: to access the opponent at position B6 use Opponent[1][5]
        (Remember python indexes from 0)

        The following convention is used for storing the state of a square:
        Unknown  = 0
        Empty    = 1
        Occupied = 2
        Missed   = 3
        Hit      = 4 (player or opponent)

        Initially, the player's board is all
        empty, the opponent's is all unknown.
        """

        self._playerBoard = [[const.EMPTY] * (6 if x < 6 else 12)
                             for x in range(12)]
        self._opponenBoard = [[const.EMPTY] * (6 if x < 6 else 12)
                              for x in range(12)]

    def deployFleet(self):
        """
        Decide where you want your fleet to
        be deployed, then return your board.
        """
        pass

    def chooseMove(self):
        """
        Decide what move to make based on current
        state of opponent's board and return it.
        """

        pass

    def setOutcome(self, entry, i1, i2):
        """
        Read the outcome of the shot from the keyboard expected
        value is const.HIT for hit and const.MISSED for missed.
        """
        pass

    def getOpponentMove(self, i1, i2):
        """
        You might like to keep track of where your
        opponent has missed, but here we just acknowledge it.
        """

        pass

    def newRound(self):
        """
        Run at the start each round.
        """
        pass

    def newPlayer(self, name=None):
        """
        Run at the start of each match, giving you the name of the opposing AI.
        """
        pass
