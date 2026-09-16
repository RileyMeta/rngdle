#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
rngdle
==============

A wordle-style RNG game

Guess a random number with wordle-style hints.

Author: Riley Ava
Created: 12/09/2026
Last Modified: 16/09/2026
Version: 1.0.0
License: MPL 2.0
Repository: https://github.com/RileyMeta/rngdle

Requirements:
    - Python 3.10 (or newer)

Usage:
    rngdle...

Copyright (c) 2026 Riley Ava
"""
import sys
from random import randrange
from collections import Counter

class Colors:
    """Colors for text"""
    RESET : str = "\033[0m"
    GREY  : str = "\033[2m"
    RED   : str = "\033[31m"
    GREEN : str = "\033[32m"
    YELLOW: str = "\033[33m"

class RNGdle:
    def __init__(self, num_range: tuple = None, limit: int = None):
        self.num_range : tuple  = num_range
        self.fail_limit: int    = limit
        random_number  : int    = randrange(self.num_range[0], self.num_range[1])
        self.number    : str    = self._left_pad(str(random_number), "0")
        self.layout    : list   = list(self.number)
        self.guesses   : list   = []

        while True:
            user_guess = self.accept_input()

            if user_guess == str(self.number):
                self.guesses.append([])
                print(f"{Colors.GREEN}Correct! The number was {self.number}.{Colors.RESET}")
                break

            user_layout: list    = list(str(user_guess))
            num_freq   : Counter = Counter(self.layout)
            self.fail_limit     -= 1

            output: list = []
            for idx, char in enumerate(user_layout):
                if char == self.layout[idx]:
                    output.append((Colors.GREEN, char))
                elif char in num_freq and num_freq[char] > 0:
                    output.append((Colors.YELLOW, char))
                    num_freq[char] -= 1
                else:
                    output.append((Colors.GREY, char))

            self.show_result(output)

            if self.fail_limit < 0:
                print(f"{Colors.RED}Game Over. The number was {self.number}.{Colors.RESET}")
                break

        self.print_final_results()

    def _left_pad(self, string: str, char: str, limit: int = 5) -> str:
        """Pad the left side of the string with a character

        Params:
            string (str): The string to pad
            char   (str): The char to pad with

        Returns:
            The char padded string
        """
        padding: int = limit - len(string)
        return str(char) * padding + string

    def accept_input(self) -> int:
        min_num: int = self.num_range[0]
        max_num: int = self.num_range[1]

        while True:
            try:
                limit     : int = self.fail_limit
                prompt    : str = f"[Remaining: {limit}] Your Guess: " if limit > 0 else "Final Guess: "
                user_input: str = input(prompt)

                if not user_input:
                    continue

                if len(user_input) != 5:
                    print("Your guess must be exactly 5 digits. Please try again.")
                    continue

                if not user_input.isdigit():
                    print("Your guess must be a number. Please try again.")
                    continue

                user_guess_str: str = str(user_input)
                user_num      : int = int(user_guess_str)

                if not 0 <= user_num <= 99999:
                    print(f"Your guess must be between 00000 and 99999. Please try again.")
                    continue

                break

            except KeyboardInterrupt:
                print()
                sys.exit(0)

        return user_guess_str

    def show_result(self, output):
        self.guesses.append(output)

        for idx, (color, num) in enumerate(output):
            print(f"[{color}{num}{Colors.RESET}]", end=" | " if idx < 4 else "\n")

    def print_final_results(self):
        if self.number in self.guesses:
            for idx, num in enumerate(str(self.number)):
                print(f"{Colors.GREEN}▆{Colors.RESET}", end=f"{" " if idx < 4 else "\n"}")
        else:
            for guess in self.guesses:
                if not guess:
                    print(f"{Colors.GREEN}▆ ▆ ▆ ▆ ▆{Colors.RESET}")
                for idx, (color, num) in enumerate(guess):
                    print(f"{color}▆{Colors.RESET}", end=f"{" " if idx < 4 else "\n"}")

if __name__ == "__main__":
    def usage():
        print()

    def help_menu():
        print("""
""")

    def version_menu():
        print("""
""")

    def main():
        argv: list = sys.argv[1:]
        argc: int  = len(argv)
        minimum: int = 0
        maximum: int = 100_000
        limit:   int = 5

        for idx, arg in enumerate(argv):
            next_arg: str = None

            if idx < argc - 1:
                next_arg = argv[idx + 1]

            if arg.startswith("-") or arg.startswith("--"):
                cur_arg = arg.replace("-", "", 2)

                match cur_arg:
                    case "help":
                        help_menu()
                        sys.exit(0)
                    case "version"|"V":
                        version_menu()
                        sys.exit(0)
                    case "min"|"m":
                        if not next_arg:
                            print("'min' requires an argument.")
                            sys.exit(1)
                        if not next_arg.isdigit():
                            print("'min' must be a number.")
                            sys.exit(1)
                        minimum = int(next_arg)
                    case "max"|"M":
                        if not next_arg:
                            print("'max' requires an argument.")
                            sys.exit(1)
                        if not next_arg.isdigit():
                            print("'max' must be a number.")
                            sys.exit(1)
                        maximum = int(next_arg)
                    case "limit"|"L":
                        if not next_arg:
                            print("'limit' requires an argument.")
                            sys.exit(1)
                        if not next_arg.isdigit():
                            print("'limit' must be a number.")
                            sys.exit(1)
                        limit = int(next_arg)

        num_range = (minimum, maximum)
        RNGdle(num_range=num_range, limit=limit)

    main()
