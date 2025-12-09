from os import system ,name

def clear_screen():
    """Clear terminal screen depending on os."""
    # if os is  windows
    if name == 'nt':
        _ = system('cls')
    else:
        _ = system('clear')

def ask_choice(prompt: str, choices: dict, aliases: dict = None):
    """
    Flexible choice parser that supports numbers and texts.
    """

    while True:
        print(prompt)
        for key, val in choices.items():
            print(f"{key}) {val}")

        answer = input("> ").strip().lower()

        if answer in choices:
            return choices[answer]

        if aliases and answer in aliases:
            key = aliases[answer]
            return choices[key]

        for key, val in choices.items():
            if answer == val.lower():
                return val

        print("Invalid choice, try again.\n")

def wait(message: str = "\nPress ENTER to continue..."):
    """Pause before returning to menu."""
    input(message)
