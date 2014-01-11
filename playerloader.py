## importing players file
import glob

def import_players():
    list_files = glob.glob("Players/*.py")
    players_files = []
    for f in list_files:
        if f.find('__init__.py')<0:
            f = f.replace("\\", '.')
            f = f.replace('/', '.')

            players_files.append(f[:-3])

    print players_files

    listPlayers = []
    player_number = 1
    for f in players_files:
        exec(("import " + f + " as player" + str(player_number)))
        player = eval(("player" + str(player_number)+".getPlayer()"))
        listPlayers.append(player)
        player_number += 1

    return listPlayers

