import random
from typing import TYPE_CHECKING
from rich.console import Console

from data import translations, synomyms
from utils import collect_user_input

if TYPE_CHECKING:
    from typing import Any

console = Console()

# ######################################################################################################################
# ######################################################################################################################


def select_words(direction: str, total_rounds: int) -> list[tuple[str, str, list[str]]]:
    '''Select words for the game'''

    if direction == 'English to Icelandic':
        return [
            (
                english,
                icelandic,
                random.sample([x[1] for x in translations if x[1] != icelandic], 2)
                + [icelandic],
            )
            for english, icelandic in random.sample(translations, total_rounds)
        ]
    else:
        return [
            (
                icelandic,
                english,
                random.sample([x[0] for x in translations if x[0] != english], 2)
                + [english],
            )
            for english, icelandic in random.sample(translations, total_rounds)
        ]


# ############################################################################################################################


def select_synomon_words(total_rounds: int) -> list[tuple[str, str, list[str]]]:
    '''Select words for the synonyms game'''

    return [
        (
            word,
            synonym,
            random.sample([x[1] for x in synomyms if x[1] != word], 2) + [synonym],
        )
        for word, synonym in random.sample(synomyms, total_rounds)
    ]


# ######################################################################################################################


def play_round(word, correct_translation, options) -> tuple['Any', 'Any']:
    '''Plays a single round by asking the user to guess the translation.
    Returns True if the answer is correct, False otherwise, and the user answer.'''

    random.shuffle(options)
    console.print(f"\n[yellow]Translate the word: {word}[/yellow]")
    for i, option in enumerate(options, 1):
        console.print(f"{i}. {option}")

    user_choice: int = collect_user_input(
        f"Choose the correct translation (1-{len(options)}): ", input_type=int
    )
    user_answer: str = options[user_choice - 1]
    return user_answer == correct_translation, user_answer


# ######################################################################################################################


def play_synonym_game(total_rounds) -> tuple[list['Any'], list['Any']]:
    """
    Plays the game for the given number of rounds in the specified direction.
    Returns a tuple of correct and incorrect results.
    """
    correct_results: list['Any'] = []
    incorrect_results: list['Any'] = []
    words: list[tuple[str, str, list[str]]] = select_synomon_words(total_rounds)

    for word, correct_translation, options in words:
        is_correct, user_answer = play_round(word, correct_translation, options)
        if is_correct:
            console.print("[green]Correct![/green]\n")
            correct_results.append((word, correct_translation))
        else:
            console.print(
                f"[red]Incorrect. The correct answer is {correct_translation}.[/red]\n"
            )
            incorrect_results.append((word, user_answer, correct_translation))

    return correct_results, incorrect_results


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
            console.print(
                f"[red]Incorrect. The correct answer is {correct_translation}.[/red]\n"
            )
            incorrect_results.append((word, user_answer, correct_translation))

    return correct_results, incorrect_results
