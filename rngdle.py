#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
rngdle
==============

A wordle-style RNG game

Guess a random number with wordle-style hints.

Author: Riley Ava
Created: 12/09/2026
Last Modified: 15/09/2026
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
    GREEN : str = "\033[32m"
    YELLOW: str = "\033[33m"

class RNGdle:
    def __init__(self):
        self.num_range : int  = (10_000, 100_000)
        self.number    : int  = randrange(self.num_range[0], self.num_range[1])
        self.layout    : list = list(str(self.number))
        self.fail_limit: int  = 5
        self.guesses   : list = []

        while True:
            user_guess = self.accept_input()

            if user_guess == self.number:
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

                if not user_input.isdigit():
                    print("Your guess must be a number. Please try again.")
                    continue

                user_num: int = int(user_input)

                if not min_num < user_num < max_num:
                    print(f"Your guess must be between {min_num} and {max_num}")
                    continue

                break

            except KeyboardInterrupt:
                print()
                sys.exit(0)

        return user_num

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
    RNGdle()
