##############################################################################
"""This is an implentation of the game "Nim". The goal of the game is to 
remove the matches in the rows. And be the one that removes the last match.
Matches can be removed from only one row each turn. And the game can be 
played in single and multiplayer."""
##############################################################################

# import the computer's move function and the tuple from the given file
from computer_functions import get_computer_move, HEAPS

# copy the tuple given in the module to a mutable list
heaps = list(HEAPS)

# set a counter variable named turn count that will decide who's turn it is
turn_count = 0

# prompt the user to pick whether to play multi player or single player
num = int(input("Please enter the number of human players (1 or 2):"))
# clause that sets the type of game and the names of players.
if num == 1:
    single_player = True
    name1 = input("Please enter your name:")
else:
    single_player = False
    name1 = input("Name of first player:")
    name2 = input("Name of second player:")


def game_winner(counter):
    """ When this function is called it decides who wins and whether to
    start a new game. If a new game is called it also decides who starts
    first."""
    # decide who played the winning turn using our counter
    if single_player:
        if counter % 2 == 1:
            print("You win")
        else:
            print("Computer wins")
    else:
        if counter % 2 == 1:
            print(name1, "wins")
        else:
            print(name2, "wins")
    # prompt user to play again
    again = input("Play again? (Y/N)")
    if again == "y" or again == "Y":
        # reset the game's list to the given list
        for i in range(len(HEAPS)):
            heaps[i] = HEAPS[i]
        # restart the game with the winner starting
        if counter % 2 == 1:
            print_board()
            counter = 0
            player_choice(counter)
        else:
            if single_player:
                counter = 0
                game_play(1, 0, counter)
            else:
                print_board()
                counter = 1
                player_choice(counter)


def print_board():
    """prints the appropriate board based on the current items in heaps"""
    for i in range(len(heaps)):
        if heaps[i] != 0:
            print(str(i+1) + ":")
            print("* " * (heaps[i]-1) + "*")
        elif heaps[i] == 0:
            print(str(i+1) + ":")
            print("")


def game_play(row, match, counter):
    """Function the takes the inputted row and match choice and removes
    matches from our board, prints the new board, and goes to the next
    person's turn"""
    # update our list to the new match counts each turn
    heaps[row - 1] = heaps[row - 1] - match
    # update our counter each turn
    counter += 1
    # checks whether all the matches are gone , and functions accordingly
    if heaps.count(0) != len(heaps):
        print_board()
        if single_player:
            if counter % 2 == 0:
                player_choice(counter)
            elif counter % 2 == 1:
                comp_move = get_computer_move(heaps)
                print("Computer takes", comp_move[1],
                      "from row", comp_move[0]+1)
                game_play(comp_move[0]+1, comp_move[1], counter)
        else:
            if counter % 2 == 0:
                player_choice(counter)
            elif counter % 2 == 1:
                player_choice(counter)
    # if the matches are all gone, calls the game_winner() function
    else:
        print_board()
        game_winner(counter)


def player_choice(counter):

    """Prompts for the user to enter the appropriate row and match choice.
    It then calls the actual game_play function with those variables and
    the counter"""
    if not single_player:
        if counter % 2 == 0:
            print(name1 + ", it's your turn:")
        else:
            print(name2 + ", it's your turn:")
    else:
        print(name1 + ", it's your turn:")

    row_choice = int(input("Row?"))
    while row_choice > len(heaps) or row_choice == 0:
        # checks whether row exists, if it doesn't, prompts again
        row_choice = int(input("Row?"))
    while heaps[row_choice - 1] == 0:
        # checks whether row choice is empty, if it is, prompts again
        print("That row is empty")
        row_choice = int(input("Row?"))
    match_choice = int(input("How many?"))
    while match_choice > heaps[row_choice - 1] or match_choice == 0:
        # checks if match choice is greater than amount of matches in row or 0
        match_choice = int(input("How many?"))
    game_play(row_choice, match_choice, counter)

print_board()
player_choice(turn_count)
