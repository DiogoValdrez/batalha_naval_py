import numpy as np
#from board import *
from functions import *

class bcolors:
    WARNING = '\033[93m'
    ENDC = '\033[0m'

def main():
    print("\t\u272E----------------------------------\u272E\n\t\u272EBem vindo ao Batalha Naval do NEEC\u272E\n\t\u272E----------------------------------\u272E\n")
    while True:
        i = start_game()
        if i == 1:
            TesteDrive()
        elif i == 2:
            PvC()
        elif i == 3:
            PvP()
        elif i == 4:
            Online()
        else:
            print("ERROR: não conhecido")
            quit()


def start_game():
    while 1:
        try:
            user_input = input("\tEscolha do modo de jogo:\n\t1.TesteDrive\t2.PvC\t3.PvP\t4.Online\n\tOu escolhe \"exit\".\n\t")
            i = int(user_input)
            if i > 4 or i < 1:
              raise Exception()
        except:
            if(user_input=='exit'): quit()
            print("{}\tEscolha de gamemode não valida.{}\n".format(bcolors.WARNING, bcolors.ENDC))
        else:
            return i

main()
