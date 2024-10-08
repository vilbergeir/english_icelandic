# Standard
from functools import reduce
import random
from typing import TYPE_CHECKING, List, Tuple, Literal

# Third-party
from rich import print
from rich.console import Console
from tabulate import tabulate

# Local
from data import translations

if TYPE_CHECKING:
    from typing import Any

# Initialize console object for rich output
console = Console()

# ######################################################################################################################
# ######################################################################################################################


def collect_user_input(prompt: str, valid_inputs: 'Any' = None, input_type: 'Any' = str) -> 'Any':
    ''' Collect user input '''
    
    while True:
        user_input: 'Any' = input(prompt).strip()
        try:
            user_input = input_type(user_input)
            if valid_inputs is None or user_input in valid_inputs:
                return user_input
            else:
                console.print(f"[red]Invalid input! Please enter one of {valid_inputs}.[/red]")
        except ValueError:
            console.print(f"[red]Please enter a valid {input_type.__name__}.[/red]")

# ######################################################################################################################

def choose_direction() -> Literal['English to Icelandic', 'Icelandic to English']:
    ''' Choose the translation direction '''
    
    valid_inputs: list[int] = [1, 2]

    console.print("Choose the translation direction: ")
    direction: 'Any' = collect_user_input("Enter 1 for English to Icelandic or 2 for Icelandic to English: ", valid_inputs, input_type=int)

    return 'English to Icelandic' if direction == 1 else 'Icelandic to English'

# ######################################################################################################################

def select_words(direction: str, total_rounds: int) -> list[tuple[str, str, list[str]]]:
    ''' Select words for the game '''

    if direction == 'English to Icelandic':
        return [(english, icelandic, random.sample([x[1] for x in translations if x[1] != icelandic], 2) + [icelandic])
                for english, icelandic in random.sample(translations, total_rounds)]
    else:
        return [(icelandic, english, random.sample([x[0] for x in translations if x[0] != english], 2) + [english])
                for english, icelandic in random.sample(translations, total_rounds)]

# ######################################################################################################################

def play_round(word, correct_translation, options) -> tuple['Any', 'Any']:
    ''' Plays a single round by asking the user to guess the translation.
    Returns True if the answer is correct, False otherwise, and the user answer. '''
    
    random.shuffle(options)
    console.print(f"\n[yellow]Translate the word: {word}[/yellow]")
    for i, option in enumerate(options, 1):
        console.print(f"{i}. {option}")

    user_choice: int = collect_user_input(f"Choose the correct translation (1-{len(options)}): ", input_type=int)
    user_answer: str = options[user_choice - 1]
    return user_answer == correct_translation, user_answer

# ######################################################################################################################

def play_game(direction, total_rounds) -> tuple[list['Any'], list['Any']]:
    """
    Plays the game for the given number of rounds in the specified direction.
    Returns a tuple of correct and incorrect results.
    """
    correct_results: list['Any'] = []
    incorrect_results: list['Any'] = []
    words: list[tuple[str, str, list[str]]] = select_words(direction, total_rounds)

    for word, correct_translation, options in words:
        is_correct, user_answer = play_round(word, correct_translation, options)
        if is_correct:
            console.print("[green]Correct![/green]\n")
            correct_results.append((word, correct_translation))
        else:
            console.print(f"[red]Incorrect. The correct answer is {correct_translation}.[/red]\n")
            incorrect_results.append((word, user_answer, correct_translation))

    return correct_results, incorrect_results

# ######################################################################################################################

def display_results(correct_results, incorrect_results):
    """
    Displays the results using rich and tabulate.
    """
    total_correct = len(correct_results)
    total_incorrect = len(incorrect_results)

    console.print(f"\n[cyan]Game Over![/cyan] [green]Correct answers: {total_correct}[/green], [red]Incorrect answers: {total_incorrect}[/red]")

    if correct_results:
        correct_table = [[word, translation] for word, translation in correct_results]
        console.print("\n[green]Words you answered correctly:[/green]")
        print(tabulate(correct_table, headers=["Word", "Correct Translation"], tablefmt="grid"))

    if incorrect_results:
        incorrect_table = [[word, user_answer, correct_answer] for word, user_answer, correct_answer in incorrect_results]
        console.print("\n[red]Words you answered incorrectly:[/red]")
        print(tabulate(incorrect_table, headers=["Word", "Your Answer", "Correct Answer"], tablefmt="grid"))

# ######################################################################################################################

def main():
    ''' Main function to run the game '''

    # Display welcome message ..
    console.print("[yellow]Welcome to the English-Icelandic translation quiz![/yellow]")

    # .. choose the translation direction ..
    direction = choose_direction()

    # .. and the number of rounds to play ..
    total_rounds = collect_user_input("How many words would you like to play? ", input_type=int)

    # .. and play the game.
    correct_results, incorrect_results = play_game(direction, total_rounds)

    # Display the game results.
    display_results(correct_results, incorrect_results)

# ######################################################################################################################

if __name__ == "__main__":
    ''' Run the main function '''
    main()
