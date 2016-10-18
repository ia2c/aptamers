fichier = open("Rosetta/main/source/src/apps.src.settings","r")
commands = fichier.readlines()
fichier.close()
commands = commands[:-1] + ["	'cifparse',\n"] + [commands[-1]]
fichier = open("Rosetta/main/source/src/apps.src.settings","w")
fichier.writelines(commands)
fichier.close()
