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

"""Number of rounds to play."""
NUM_ROUNDS = 1


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

    def __init__(self):
        self.move_index = 0
        self.my_move = moves

    def move(self):
        my_move = moves[self.move_index]
        self.move_index = (self.move_index + 1) % len(self.my_move)
        return my_move

    def learn(self, my_move, their_move):
        pass


"""This function tracks what moves beat the other"""


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
        self.rounds = 3
        for round in range(self.rounds):
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
                  f"Player 2 Final Score: {self.p2_score}")
        if self.p1_score < self.p2_score:
            print(f"{Fore.RED}Player 2 wins the game!\n"
                  f"Final Score: {self.p2_score}{Style.RESET_ALL}\n"
                  f"{Fore.MAGENTA}Player 1 Final Score: {self.p1_score}\n"
                  f"{Style.RESET_ALL}")


"""This block of code sets up the game with a human player and

three rounds against random computer players. The game is played

three times with different computer players each time."""


if __name__ == '__main__':
    # Initialize a Game object with a Human player and None as the opponent
    game = Game(Human(), None)
    while True:
        # Ask the user to choose an opponent
        print("Please choose your opponent:\n"
              "1. Random Player\n"
              "2. Reflect Player\n"
              "3. Cycle Player\n")

        player_choice = valid_input("Enter 1, 2 or 3: ", ["1", "2", "3"])

        if player_choice == "1":
            game.p2 = Random()
            break
        elif player_choice == "2":
            game.p2 = Reflect()
            break
        elif player_choice == "3":
            game.p2 = Cycle()
            break
        else:
            print("Invalid input. Please try again.")
            continue

    # Play rounds of the game
    for play in range(NUM_ROUNDS):
        # Play the game
        game.play_game()

        # Ask the user if they want to play again
        play_again = valid_input("Would you like to play again? (y/n): ",
                                 ["y", "n"])
        if play_again == "y":
            game.play_game()
        else:
            print("Thanks for playing!")
            break
