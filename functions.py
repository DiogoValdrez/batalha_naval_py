from board import *
import random

MAX_rondas = 50
Game_mode = 0

###############################################################################################
# Estas funções são as funções correspondentes a cada modo de jogo
# Para já vamos fazer a função que corresponde à criação de um taboleiro por parte do computador e o utilizador fica a adivinhar quais as posições dos barcos

def TesteDrive():
    counter_jogadas = 1

    check = True

    tab = tabuleiro("computador")
    generate_board(tab)
    tab.print_tabuleiro("enemy")

    print("{}\tTabuleiro criado, é a vez do jogador jogar.{}\n".format(bcolors.OKBLUE, bcolors.ENDC))
    while check:
        make_play(tab)
        center_print(23, "Balas restantes: {}".format(MAX_rondas-counter_jogadas), bcolors.HEADER, 1)
        tab.print_tabuleiro("enemy")
        counter_jogadas += 1
        check = False
        for i in tab.boat_list:
            if i.state == True:
                check = True
                continue
        if counter_jogadas > MAX_rondas and check == True:
            print("{}\n\tPerdeste o jogo. Não conseguiste acertar em todos os barcos antes das balas acabarem.{}\n".format(bcolors.FAIL, bcolors.ENDC))
            return 0

    print("{}\n\tParabéns venceste o jogo ainda com {} rondas por jogar.{}\n".format(bcolors.OKGREEN, MAX_rondas-counter_jogadas, bcolors.ENDC))
    return 1


def PvC():
    counter_jogadas = 1

    check = False

    tab_pc = tabuleiro("computador")
    generate_board(tab_pc)
    tab_player = tabuleiro("Player")
    generate_board(tab_player)
    tab_player.print_tabuleiro2(tab_pc)

    while True:
        bot_d = bot_play(tab_player)

        check = True
        for i in tab_pc.boat_list:
            if i.state == True:
                check = False
                continue

        if check:
            print("{}\n\tPerdeste o jogo. Todos os teus barcos foram afundados.{}\n".format(bcolors.FAIL, bcolors.ENDC))
            return 0

        print("{}\n\tRonda do player:{}\n".format(bcolors.OKGREEN, bcolors.ENDC))
        player_d = make_play(tab_pc)

        if bot_d == 'Destroyed' and player_d == 'Destroyed':
            center_print2(23, "Destroyed", bcolors.FAIL, 1, 1)
        elif bot_d == 'Destroyed':
            center_print(23, "Destroyed", bcolors.FAIL, 1)
        elif player_d == 'Destroyed':
            center_print(23, "Destroyed", bcolors.FAIL, 8)
        tab_player.print_tabuleiro2(tab_pc)

        check = True
        for i in tab_pc.boat_list:
            if i.state == True:
                check = False
                continue

        if check:
            print("{}\n\tParabéns venceste o jogo após {} rondas.{}\n".format(bcolors.OKGREEN, counter_jogadas, bcolors.ENDC))
            return 1

        counter_jogadas += 1


def PvP():
    print("{}\tNão implementado.{}\n".format(bcolors.FAIL, bcolors.ENDC))

def Online():
    print("{}\tNão implementado.{}\n".format(bcolors.FAIL, bcolors.ENDC))


###############################################################################################
# Esta função corresponde a criação e inserção dos barcos no tabuleiro
# Para já esta função vai estar a criar um tabuleiro automaticamente. Mais para a frente pode vir a ser feito a parte de o utilizador fazer o seu taboleiro

def generate_board(table):
    inp = 'M'
    if table.name != "computador":
        valid = False
        while not valid:
            inp = input("\n\tEscolhe como queres meter os barcos (M - manual; A - automático): ")
            if inp.upper() == 'M' or inp.upper() == 'A':
                valid = True

    letters = ('A','B','C','D','E','F','G','H','I','J','a','b','c','d','e','f','g','h','i','j')
    numbers = (1,2,3,4,5,6,7,8,9,10)

    boat_sizes = (2, 2, 2, 2, 3, 3 ,3, 4, 4, 5)
    boat_orientations = ('vertical', 'horizontal')

    if table.name == "computador" or inp.upper() == 'A':
        for i in boat_sizes:
            valid = False
            while not valid:
                orientation = random.choice(boat_orientations)
                if orientation == 'vertical':
                    row = random.randint(0, Size_Board-i)
                    column = random.randint(0, Size_Board-1)
                    if table.insert_boat(row, column, i, 'vertical'):
                        valid = True
                else:
                    row = random.randint(0, Size_Board-1)
                    column = random.randint(0, Size_Board-i)
                    if table.insert_boat(row, column, i, 'horizontal'):
                        valid = True

        if table.name != "computador":
            table.print_tabuleiro("friend")
    else:
        table.print_tabuleiro("friend")
        for i in boat_sizes:
            valid = False
            while not valid:
                play =  input("\n\tEscolhe a posição inicial do barco de tamanho {}:".format(i))
                if (len(play) != 2 and len(play) != 3) or not play[0].isalpha() or not play[1:].isdigit() or play[0] not in letters or int(play[1:]) not in numbers:
                    print("\n\tInput invalido. As cordenadas devem ser uma letra (A-J) seguidas de um número (1-10).")
                else:
                    orientation = input("\n\tEscolhe a orientação do barco (H ou V):")
                    if orientation not in ['H','V','h','v']:
                        print("\n\tA orientação deve ser H se horizontal ou V se vertical")
                    else:
                        play = play.upper()
                        column = letters.index(play[0])
                        row = numbers.index(int(play[1:]))
                        if orientation == 'V' or orientation == 'v':
                            if row+i > Size_Board: row = row - (i - 1)
                            if table.insert_boat(row, column, i, "vertical"):
                                valid = True
                            else: print("\n\tJá existe um barco por baixo daquele que queres meter")
                        elif orientation == 'H' or orientation == 'h':
                            while column+i > Size_Board: column = column - (i - 1)
                            if table.insert_boat(row, column, i, "horizontal"):
                                valid = True
                            else: print("\n\tJá existe um barco por baixo daquele que queres meter")
            table.print_tabuleiro("friend")



###############################################################################################
# Esta função verifica se a escolha das coordenada à qual se quer disparar é válida
#

def make_play(table_pc):
    shot = tuple()
    play = list(shot)
    letters = ('A','B','C','D','E','F','G','H','I','J','a','b','c','d','e','f','g','h','i','j')
    numbers = (1,2,3,4,5,6,7,8,9,10)
    valid = False
    while not valid:
        valid = True
        play =  input('\n\tPlease choose the target coordinates: ')
        if (len(play) != 2 and len(play) != 3) or not play[0].isalpha() or not play[1:].isdigit() or play[0] not in letters or int(play[1:]) not in numbers:
            valid = False
            print('\n\tInvalid input. Coordinates must be a letter (A-J) followed by a number (1-10).')
            continue
        if not table_pc.check_hit(int(play[1:])-1, letter_to_pose(play[0])):
            valid = False
            print('\n\tInvalid input. You already shot in those coordinates.')
            continue
    if table_pc.shoot(int(play[1:])-1, letter_to_pose(play[0])) == 'Destroyed':
        return 'Destroyed'

    return 0



def letter_to_pose(letter):
    let = np.array(['A','B','C','D','E','F','G','H','I','J','a','b','c','d','e','f','g','h','i','j'])

    column = int(np.where(let == letter)[0])

    if column > 9:
        column = column - 10

    return column


def bot_play(table_pc):
    shot = tuple()
    play = list(shot)
    letters = ('A','B','C','D','E','F','G','H','I','J','a','b','c','d','e','f','g','h','i','j')
    numbers = (1,2,3,4,5,6,7,8,9,10)
    valid = False
    while not valid:
        valid = True
        play = "{}{}".format(random.choice(letters), random.choice(numbers))
        if not table_pc.check_hit(int(play[1:])-1, letter_to_pose(play[0])):
            valid = False
            continue
    if table_pc.shoot(int(play[1:])-1, letter_to_pose(play[0])) == 'Destroyed':
        return 'Destroyed'

    return 0


def center_print(num, text, clr, tab_num):
    st = text.center(num)
    tab = ''

    for i in range(tab_num):
        tab += '\t'

    if clr != -1:
        print("\n{}{}{}{}".format(tab, clr, st, bcolors.ENDC))
    else:
        print("\n{}{}".format(tab, st))


def center_print2(num, text, clr, tab_num1, tab_num2):
    st = text.center(num)
    tab1 = ''
    tab2 = ''

    for i in range(tab_num1):
        tab1 += '\t'

    for i in range(tab_num2):
        tab2 += '\t'

    if clr != -1:
        print("\n{}{}{}{}{}".format(tab1, clr, st, tab2, st, bcolors.ENDC))
    else:
        print("\n{}{}{}{}".format(tab1, st, tab2, st))
