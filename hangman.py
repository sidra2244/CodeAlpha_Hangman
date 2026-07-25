"""
HANGMAN — Terminal Edition
A modern, colorful take on the classic word-guessing game.

Key concepts used: random, while loop, if-else, strings, lists
"""

import random
import os

# ---------------------------------------------------------
# Enable ANSI colors on Windows terminals too
# ---------------------------------------------------------
os.system("")

# ---------------------------------------------------------
# Colors (plain ANSI escape codes — no external libraries)
# ---------------------------------------------------------
class Color:
    RESET = "\033[0m"
    BOLD = "\033[1m"
    GREEN = "\033[92m"
    RED = "\033[91m"
    YELLOW = "\033[93m"
    CYAN = "\033[96m"
    MAGENTA = "\033[95m"
    GRAY = "\033[90m"


# ---------------------------------------------------------
# Word bank — grouped by category for a bit of variety
# ---------------------------------------------------------
WORD_BANK = {
    "Programming": ["python", "variable", "function", "loop", "array"],
    "Animals": ["elephant", "giraffe", "dolphin", "penguin", "kangaroo"],
    "Countries": ["pakistan", "germany", "brazil", "canada", "japan"],
}

MAX_WRONG_GUESSES = 6

# ---------------------------------------------------------
# ASCII art for each stage of the hangman (0 to 6 wrong guesses)
# ---------------------------------------------------------
HANGMAN_STAGES = [
    """
       ------
       |    |
       |
       |
       |
       |
    ---------
    """,
    """
       ------
       |    |
       |    O
       |
       |
       |
    ---------
    """,
    """
       ------
       |    |
       |    O
       |    |
       |
       |
    ---------
    """,
    """
       ------
       |    |
       |    O
       |   /|
       |
       |
    ---------
    """,
    """
       ------
       |    |
       |    O
       |   /|\\
       |
       |
    ---------
    """,
    """
       ------
       |    |
       |    O
       |   /|\\
       |   /
       |
    ---------
    """,
    """
       ------
       |    |
       |    O
       |   /|\\
       |   / \\
       |
    ---------
    """,
]


def clear_screen():
    """Clears the terminal so each round feels fresh."""
    os.system("cls" if os.name == "nt" else "clear")


def print_banner():
    banner = f"""
{Color.CYAN}{Color.BOLD}
 _   _   _   _   _   _   _   _   _   _
( H )( A )( N )( G )( M )( A )( N )
 \\_/ \\_/ \\_/ \\_/ \\_/ \\_/ \\_/
{Color.RESET}{Color.GRAY}          -- Terminal Edition --{Color.RESET}
"""
    print(banner)


def choose_word():
    """Randomly picks a category, then a random word from it."""
    category = random.choice(list(WORD_BANK.keys()))
    word = random.choice(WORD_BANK[category])
    return word.lower(), category


def build_display_word(word, guessed_letters):
    """
    Builds the underscore/letter display, e.g. p y t _ o n
    using a list comprehension over the string.
    """
    display = [letter if letter in guessed_letters else "_" for letter in word]
    return " ".join(display)


def draw_hangman(wrong_count):
    print(f"{Color.YELLOW}{HANGMAN_STAGES[wrong_count]}{Color.RESET}")


def print_status(word, guessed_letters, wrong_count, wrong_letters, category):
    clear_screen()
    print_banner()
    print(f"{Color.MAGENTA}Category:{Color.RESET} {category}\n")
    draw_hangman(wrong_count)
    print(f"{Color.BOLD}Word: {Color.CYAN}{build_display_word(word, guessed_letters)}{Color.RESET}\n")
    print(f"{Color.RED}Wrong guesses left: {MAX_WRONG_GUESSES - wrong_count}{Color.RESET}")

    if wrong_letters:
        print(f"{Color.GRAY}Wrong letters used: {', '.join(sorted(wrong_letters))}{Color.RESET}")
    print()


def get_valid_guess(guessed_letters):
    """
    Keeps asking until the player enters a single, new, alphabetic letter.
    Demonstrates while loop + if-else working together.
    """
    while True:
        guess = input(f"{Color.BOLD}Guess a letter: {Color.RESET}").strip().lower()

        if len(guess) != 1 or not guess.isalpha():
            print(f"{Color.RED}Please enter a single letter (a-z).{Color.RESET}")
        elif guess in guessed_letters:
            print(f"{Color.YELLOW}You already guessed '{guess}'. Try another.{Color.RESET}")
        else:
            return guess


def play_round():
    word, category = choose_word()
    guessed_letters = []
    wrong_letters = []
    wrong_count = 0

    # Main game loop — keeps running until win or loss
    while wrong_count < MAX_WRONG_GUESSES:
        print_status(word, guessed_letters, wrong_count, wrong_letters, category)

        # Check win condition before asking for more input
        if all(letter in guessed_letters for letter in word):
            break

        guess = get_valid_guess(guessed_letters)
        guessed_letters.append(guess)

        if guess in word:
            print(f"{Color.GREEN}Nice! '{guess}' is in the word.{Color.RESET}")
        else:
            wrong_count += 1
            wrong_letters.append(guess)
            print(f"{Color.RED}Nope, no '{guess}' here.{Color.RESET}")

        input(f"{Color.GRAY}Press Enter to continue...{Color.RESET}")

    # Final screen
    print_status(word, guessed_letters, wrong_count, wrong_letters, category)

    if wrong_count >= MAX_WRONG_GUESSES:
        print(f"{Color.RED}{Color.BOLD}💀 Game Over! The word was: {word.upper()}{Color.RESET}\n")
        return False
    else:
        print(f"{Color.GREEN}{Color.BOLD}🎉 You won! The word was: {word.upper()}{Color.RESET}\n")
        return True


def main():
    wins = 0
    losses = 0

    while True:
        won = play_round()
        if won:
            wins += 1
        else:
            losses += 1

        print(f"{Color.CYAN}Score → Wins: {wins}  Losses: {losses}{Color.RESET}\n")

        again = input(f"{Color.BOLD}Play again? (y/n): {Color.RESET}").strip().lower()
        if again != "y":
            print(f"\n{Color.MAGENTA}Thanks for playing! Final score — Wins: {wins}, Losses: {losses}{Color.RESET}")
            break


if __name__ == "__main__":
    main()
