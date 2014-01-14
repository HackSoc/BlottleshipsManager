import glob
import imp
import os
import const


class BasePlayer:
    def __init__(self, name="Unknown", year=1,
                 version="1.0", description="None"):
        """
        Initialise the boards: player to empty, opponent to unknown.

        name: Can be whatever you want as long as it is a sensible
              one, and no more than 25 characters.
        year: Indicate your year of study here should range from 1 to 4.
        version: The version of your solution if you have more than one.
        description: A description of how your player works.
        """

        self.name = name
        self.year = year
        self.version = version
        self.description = description

        # The boards are stored in a "jagged" 2 dimensional list
        # Example: to access the opponent at position B6 use Opponent[1][5]
        # (Remember python indexes from 0)
        #
        # The following convention is used for storing the state of a square:
        # Unknown  = 0
        # Empty    = 1
        # Occupied = 2
        # Missed   = 3
        # Hit      = 4 (player or opponent)
        #
        # Initially, the player's board is all
        # empty, the opponent's is all unknown.

        self.board = [[const.EMPTY] * (6 if x < 6 else 12)
                      for x in range(12)]
        self.opponent_board = [[const.UNKNOWN] * (6 if x < 6 else 12)
                               for x in range(12)]

    def deployFleet(self):
        """
        Decide where you want your fleet to
        be deployed.
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


def load():
    list_files = glob.glob("Players/*.py")

    players_files = [('./' + f, f.replace(os.sep, '.')[:-3])
                     for f in list_files
                     if "__init__" not in f]

    listPlayers = []
    for fname, mname in players_files:
        mod = imp.load_source(mname, fname)
        listPlayers.append(mod.getPlayer())

    return listPlayers
