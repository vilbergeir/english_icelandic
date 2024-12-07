# Standard
from functools import reduce
import random
from typing import TYPE_CHECKING

# Third-party
from rich import print
from rich.console import Console
from tabulate import tabulate

# Local
from utils import collect_user_input, choose_direction, display_results, choose_game
from game import play_game, play_synonym_game

if TYPE_CHECKING:
    from typing import Any

# Initialize console object for rich output
console = Console()

# ######################################################################################################################
# ######################################################################################################################


def choose_game() -> str:
    '''Allows the user to choose which game to play.'''
    console.print("[yellow]Choose a game to play:[/yellow]")
    console.print("1. English-Icelandic Translation Quiz")
    console.print("2. Synonyms Game")
    game_choice = collect_user_input(
        "Enter the number of your choice: ", input_type=int
    )
    if game_choice == 1:
        return "translation"
    elif game_choice == 2:
        return "synonyms"
    else:
        console.print("[red]Invalid choice. Defaulting to Translation Quiz.[/red]")
        return "translation"

    # ############################################################################################################################


def main() -> None:
    '''Main function to run the game'''

    # Display welcome message ..
    console.print("[yellow]Welcome to the English-Icelandic translation quiz![/yellow]")

    game: str = choose_game()

    if game == "translation":
        # .. choose the translation direction ..
        direction = choose_direction()

        # .. and the number of rounds to play ..
        total_rounds: int = collect_user_input(
            "How many words would you like to play? ", input_type=int
        )

        # .. and play the game.
        correct_results, incorrect_results = play_game(direction, total_rounds)

    elif game == "synonyms":
        # .. and the number of rounds to play ..
        total_rounds = collect_user_input(
            "How many words would you like to play? ", input_type=int
        )

        # .. and play the synonyms game.
        correct_results, incorrect_results = play_synonym_game(total_rounds)

    # Display the game results.
    display_results(correct_results, incorrect_results)


# ######################################################################################################################

if __name__ == "__main__":
    '''Run the main function'''
    main()
