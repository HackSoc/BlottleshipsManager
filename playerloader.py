# Import players files
import glob
import imp
import os

import Players


class PlayerWrapper:
    def __init__(self, player):
        self.ai = player
        self.stats = {}
        self.reset_stats()

    def reset_stats(self):
        self.stats["Win"] = 0
        self.stats["Draw"] = 0
        self.stats["Loss"] = 0
        self.stats["For"] = 0
        self.stats["Against"] = 0

    def score(self):
        pass


def import_players():
    list_files = glob.glob("Players/*.py")

    players_files = [('./' + f, f.replace(os.sep, '.')[:-3])
                     for f in list_files
                     if "__init__" not in f]

    listPlayers = []
    for fname, mname in players_files:
        mod = imp.load_source(mname, fname)
        listPlayers.append(PlayerWrapper(mod.getPlayer()))

    return listPlayers
