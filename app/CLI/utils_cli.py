from os import system ,name

def clear_screen():
    """Clear terminal screen depending on os."""
    # if os is  windows
    if name == 'nt':
        _ = system('cls')
    else:
        _ = system('clear')

def ask_choice(prompt, choices: dict):
    """
    Gives a chocie and returns it.
    """
    while True:
        print(prompt)
        for key, val in choices.items():
            print(f"{key}) {val}")
        answer = input("> ").strip()

        if answer in choices:
            return choices[answer]

        print("Invalid choice, try again.\n")

def wait(message: str = "\nPress ENTER to continue..."):
    """Pause before returning to menu."""
    input(message)
