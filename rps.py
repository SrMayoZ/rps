#!/usr/bin/env python3

import random

from unicodedata import name
from colorama import Fore, Style

"""This function validates user input"""


def valid_input(prompt, options):
    while True:
        option = input(prompt).lower()
        if option in options:
            return option
        print(f'The option "{option}" is invalid. Try again!')


"""This program plays a game of Rock, Paper, Scissors between two Players,
and reports both Player's scores each round."""

moves = ['rock', 'paper', 'scissors']

"""The Player class is the parent class for all of the Players
in this game"""


class Player:

    def move(self):
        return 'rock'

    def learn(self, my_move, their_move):
        pass


"""This class is a subclass of the Player class, assigns
 a random move by the player."""


class Random(Player):

    def move(self):
        return random.choice(moves)

    def learn(self, my_move, their_move):
        pass


"""This subclass is a human player that inherits from the Player class."""


class Human(Player):

    def move(self):
        return valid_input("Rock, Paper or Scissors?\n", moves)

    def learn(self, my_move, their_move):
        pass


"""This learns the opponent's previous move and plays it in next round."""


class Reflect(Player):
    def __init__(self):
        self.their_move = None  # Opponent's last move
    # Inherits from Player class, learns the opposing players
    #  move to use for it's next move.

    def move(self):
        if self.their_move is None:
            return random.choice(moves)
        return self.their_move

    # This method stores opponents last
    def learn(self, my_move, their_move):
        self.their_move = their_move


"""This subclass is responsible for cycling to the next move."""


class Cycle(Player):
    # Dunder method. Assigns the next move to the
    # possible outcome of moves.
    def __init__(self):
        self.my_next_move_index = random.randrange(3)

    # We use modulo to cycle through each move.
    # We do not want to choose the same move twice.

    def move(self):
        my_move = moves[self.my_next_move_index]
        self.my_next_move_index = (self.my_next_move_index + 1) % 3
        return my_move


"""This function tracks what moves beat the other!"""


def beats(one, two):

    return ((one == 'rock' and two == 'scissors') or
            (one == 'scissors' and two == 'paper') or
            (one == 'paper' and two == 'rock'))


class Game:
    """This line of code is defining class-level variables that
    will be used to keep track of the scores and total score in the game."""
    p1_score = 0
    p2_score = 0

    def __init__(self, p1, p2):
        self.p1 = p1
        self.p2 = p2

    def play_round(self):
        move1 = self.p1.move()
        move2 = self.p2.move()
        print(f"{Fore.YELLOW}Player 1: {move1}  {Fore.MAGENTA}Player 2:\n"
              f"{move2}{Style.RESET_ALL}")
        self.p1.learn(move1, move2)
        self.p2.learn(move2, move1)

        if move1 == move2:
            print("This round is a tie!\n"
                  f"Player 1 Score: {self.p1_score}\n"
                  f"Player 2 Score: {self.p2_score}")

        elif beats(move1, move2):
            self.p1_score += 1
            print(f"{Fore.GREEN}Player 1 Wins!{Style.RESET_ALL}\n"
                  f"{Fore.YELLOW}Player 1 Score: {self.p1_score}\n"
                  f"{Style.RESET_ALL}\n"
                  f"{Fore.MAGENTA}Player 2 Score: {self.p2_score}\n"
                  f"{Style.RESET_ALL}")

        if beats(move2, move1):
            self.p2_score += 1
            print(f"{Fore.GREEN}Player 2 wins{Style.RESET_ALL}\n"
                  f"Player 1 Score: {self.p1_score}\n"
                  f"Player 2 Score: {self.p2_score}")

    def random_player(self):
        player_type = random.choice(["random", "reflect", "cycle"])
        if player_type == "random":
            return Random()
        elif player_type == "reflect":
            return Reflect()
        else:
            return Cycle()

    def play_game(self):
        print(f"{Fore.RED}Welcome to Rock, Paper & Scissors\n"
              f"game!{Style.RESET_ALL}\n")
        for round in range(3):
            print(f"Round {round + 1}:")
            self.play_round()
        print("Game over!")

        # This section of the code determines the winner of the game.

        if self.p1_score == self.p2_score:
            print(f"{Fore.CYAN}This game ends in a tie!{Style.RESET_ALL}\n"
                  f"Player 1 Score: {self.p1_score}\n"
                  f"{Fore.MAGENTA}Player 2 Score: {self.p2_score}\n"
                  f"{Style.RESET_ALL}")
        elif self.p1_score > self.p2_score:
            print(f"{Fore.RED}Player 1 wins the game!\n"
                  f"Final Score: {self.p1_score}{Style.RESET_ALL}\n"
                  f"Play 2 Final Score: {self.p2_score}")
        if self.p1_score < self.p2_score:
            print(f"{Fore.RED}Player 2 wins the game!\n"
                  f"Final Score: {self.p2_score}{Style.RESET_ALL}\n"
                  f"{Fore.MAGENTA}Player 1 Final Score: {self.p1_score}\n"
                  f"{Style.RESET_ALL}")


if __name__ == '__main__':
    game = Game(Human(), None)
    for i in range(3):
        game.p2 = game.random_player()
        game.play_game()
