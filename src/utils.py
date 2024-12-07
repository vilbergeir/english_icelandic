from typing import TYPE_CHECKING
from rich.console import Console
from tabulate import tabulate

if TYPE_CHECKING:
    from typing import Any, Literal

# ######################################################################################################################
# ######################################################################################################################

console = Console()


def collect_user_input(
    prompt: str, valid_inputs: 'Any' = None, input_type: 'Any' = str
) -> 'Any':
    '''Collect user input'''

    while True:
        user_input: 'Any' = input(prompt).strip()
        try:
            user_input = input_type(user_input)
            if valid_inputs is None or user_input in valid_inputs:
                return user_input
            else:
                console.print(
                    f"[red]Invalid input! Please enter one of {valid_inputs}.[/red]"
                )
        except ValueError:
            console.print(f"[red]Please enter a valid {input_type.__name__}.[/red]")


# ######################################################################################################################


def choose_direction() -> 'Literal["English to Icelandic", "Icelandic to English"]':
    '''Choose the translation direction'''

    valid_inputs: list[int] = [1, 2]

    console.print("Choose the translation direction: ")
    direction: 'Any' = collect_user_input(
        "Enter 1 for English to Icelandic or 2 for Icelandic to English: ",
        valid_inputs,
        input_type=int,
    )

    return 'English to Icelandic' if direction == 1 else 'Icelandic to English'


# ######################################################################################################################


def choose_game() -> 'Literal["Synonyms", "Translations"]':
    '''Choose the game type'''

    valid_inputs: list[int] = [1, 2]

    console.print("Choose the game type: ")
    game: 'Any' = collect_user_input(
        "Enter 1 for Translations or 2 for Synonyms: ", valid_inputs, input_type=int
    )

    return 'Translations' if game == 1 else 'Synonyms'


# ######################################################################################################################


def display_results(correct_results, incorrect_results):
    """
    Displays the results using rich and tabulate.
    """
    total_correct = len(correct_results)
    total_incorrect = len(incorrect_results)

    console.print(
        f"\n[cyan]Game Over![/cyan] [green]Correct answers: {total_correct}[/green], [red]Incorrect answers: {total_incorrect}[/red]"
    )

    if correct_results:
        correct_table = [[word, translation] for word, translation in correct_results]
        console.print("\n[green]Words you answered correctly:[/green]")
        print(
            tabulate(
                correct_table, headers=["Word", "Correct Translation"], tablefmt="grid"
            )
        )

    if incorrect_results:
        incorrect_table = [
            [word, user_answer, correct_answer]
            for word, user_answer, correct_answer in incorrect_results
        ]
        console.print("\n[red]Words you answered incorrectly:[/red]")
        print(
            tabulate(
                incorrect_table,
                headers=["Word", "Your Answer", "Correct Answer"],
                tablefmt="grid",
            )
        )
