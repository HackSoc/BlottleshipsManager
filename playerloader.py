# Import players files
import glob
import imp
import os
import Players


def import_players():
    list_files = glob.glob("Players/*.py")

    players_files = [('./' + f, f.replace(os.sep, '.')[:-3])
                     for f in list_files
                     if "__init__" not in f]

    listPlayers = []
    for fname, mname in players_files:
        mod = imp.load_source(mname, fname)
        listPlayers.append(mod.getPlayer())

    return listPlayers
